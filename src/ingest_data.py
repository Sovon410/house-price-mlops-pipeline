import os
import zipfile
from abc import ABC, abstractmethod

import pandas as pd

# Define the abstract class for data ingestor.
class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        pass


# Implement a concrete class for ZIP Ingestion
class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        """Extracts a .zip file and returns the content as a pandas DataFrame."""
        # Ensure the file is a .zip
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a zip file.")
        
        # Extract the zip file.
        with zipfile.ZipFile(file= file_path, mode= "r") as zip_ref:
            zip_ref.extractall("extracted_data")
            
        # Find the extracted csv file (assuming there is one CSV file inside the zip).
        extraxted_files = os.listdir("extracted_data")
        csv_files = [file for file in extraxted_files if file.endswith(".csv")]
        
        if len(csv_files) == 0:
            raise FileNotFoundError("No CSV file found in the extracted data.")
        if len(csv_files) > 1:
            raise ValueError("Multiple CSV files found. Please specify which one to use.")
        
        # Read the CSV into a DataFrame.
        csv_file_path = os.path.join("extracted_data", csv_files[0])
        df = pd.read_csv(csv_file_path)
        
        
        # Return the dataframe
        return df
    

# Implement a Factory to create DataIngestors
class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        """Returns the appropriate DataIngestor based on file extension."""
        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"No ingestor available for file extension: {file_extension}")
        
        
# Example usage.
if __name__ == "__main__":
    # # Specify the file path
    # file_path = r"C:\MY_WORKSPACE\New folder\House-Price-Prediction\prices-predictor-system\data\archive.zip"
    
    # # Determine the file extension.
    # file_extension = os.path.splitext(file_path)[1]
    
    # # Get the appropriate DataIngestor.
    # data_ingestor = DataIngestorFactory.get_data_ingestor(file_extension)
    
    # # Ingest the data and load it into a DataFrame
    # df = data_ingestor.ingest(file_path=file_path)
    
    # print("\n")
    # # Now df contains the DataFrame from the extracted CSV
    # print(df.head(10))          # Display the first few rows of the DataFrame
    # print("\n")
    pass