import json
import logging
import os
import pandas as pd
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MLFLOW_PREDICT_URL = "http://127.0.0.1:8000/invocations"
MODEL_URI = os.path.expanduser(
    "~/AppData/Roaming/zenml/local_stores/0217948e-b21e-4af3-a5b4-0d4abccd3a26/mlruns/430502628820827892/897a1668458548829dc9ecb335e7d95a/artifacts/model"
)

# Try loading the model directly into memory for offline / resilient serving
direct_model = None
try:
    import mlflow.pyfunc
    if os.path.exists(MODEL_URI):
        direct_model = mlflow.pyfunc.load_model(MODEL_URI)
        print("✅ Local MLflow model loaded directly into Web App memory.")
except Exception as e:
    print(f"ℹ️ Could not load direct model into memory ({e}). Will proxy to port 8000.")

DOUBLE_COLS = [
    "Lot Frontage", "Mas Vnr Area", "BsmtFin SF 1", "BsmtFin SF 2",
    "Bsmt Unf SF", "Total Bsmt SF", "Gr Liv Area", "Bsmt Full Bath",
    "Bsmt Half Bath", "Garage Yr Blt", "Garage Cars", "Garage Area"
]

# Baseline record matching model expectations
DEFAULT_FEATURES = {
    "Order": 1,
    "PID": 5286,
    "MS SubClass": 20,
    "Lot Frontage": 80.0,
    "Lot Area": 9600,
    "Overall Qual": 7,
    "Overall Cond": 5,
    "Year Built": 2005,
    "Year Remod/Add": 2006,
    "Mas Vnr Area": 120.0,
    "BsmtFin SF 1": 700.0,
    "BsmtFin SF 2": 0.0,
    "Bsmt Unf SF": 150.0,
    "Total Bsmt SF": 850.0,
    "1st Flr SF": 856,
    "2nd Flr SF": 854,
    "Low Qual Fin SF": 0,
    "Gr Liv Area": 1710.0,
    "Bsmt Full Bath": 1.0,
    "Bsmt Half Bath": 0.0,
    "Full Bath": 2,
    "Half Bath": 1,
    "Bedroom AbvGr": 3,
    "Kitchen AbvGr": 1,
    "TotRms AbvGrd": 7,
    "Fireplaces": 1,
    "Garage Yr Blt": 2005.0,
    "Garage Cars": 2.0,
    "Garage Area": 500.0,
    "Wood Deck SF": 210,
    "Open Porch SF": 45,
    "Enclosed Porch": 0,
    "3Ssn Porch": 0,
    "Screen Porch": 0,
    "Pool Area": 0,
    "Misc Val": 0,
    "Mo Sold": 6,
    "Yr Sold": 2010,
}

@app.route("/")
def index():
    return render_template("index.html", defaults=DEFAULT_FEATURES)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        user_input = request.json or {}
        payload = DEFAULT_FEATURES.copy()

        # Update with values received from user form
        for key, value in user_input.items():
            if key in payload and value != "":
                if key in DOUBLE_COLS:
                    payload[key] = float(value)
                else:
                    payload[key] = int(float(value))

        raw_prediction = None

        # Strategy 1: Predict directly using in-memory model (fast & independent)
        if direct_model is not None:
            df = pd.DataFrame([payload])
            for col in DOUBLE_COLS:
                if col in df.columns:
                    df[col] = df[col].astype("float64")
            preds = direct_model.predict(df)
            raw_prediction = float(preds[0]) if hasattr(preds, "__iter__") else float(preds)

        # Strategy 2: If in-memory not available, proxy to MLflow HTTP endpoint
        if raw_prediction is None:
            response = requests.post(
                MLFLOW_PREDICT_URL,
                headers={"Content-Type": "application/json"},
                json={"dataframe_records": [payload]},
                timeout=4
            )
            if response.status_code == 200:
                result = response.json()
                raw_prediction = float(result.get("predictions", [0])[0])
            else:
                return jsonify({
                    "success": False,
                    "error": f"MLflow error ({response.status_code}): {response.text}"
                }), 502

        # Format output
        # Model predicts on transformed/normalized scale (~280 -> ~$280,000)
        formatted_val = f"${raw_prediction * 1000:,.0f}" if raw_prediction < 1000 else f"${raw_prediction:,.0f}"

        return jsonify({
            "success": True,
            "prediction": raw_prediction,
            "formatted": formatted_val
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

import threading
import webbrowser

if __name__ == "__main__":
    url = "http://127.0.0.1:5001"
    print("\n" + "=" * 62)
    print(" 🏡 Ames House Price Prediction Web UI")
    print(f" 🚀 Automatically launching in your browser: {url}")
    print("=" * 62 + "\n")

    # Automatically open default browser after a brief delay for server initialization
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()

    app.run(host="127.0.0.1", port=5001, debug=False)
