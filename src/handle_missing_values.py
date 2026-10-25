import logging
from abc import ABC, abstractmethod
import pandas as pd


# Setup loggiong configuration
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s"
)



# Abstract base class fore Missing value handling strategy
class MissingValueHandlingStrategy(ABC):
    @abstractmethod
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to handle missing values in the DataFrame.

        Parameters:
        df (pd.DataFrame): The input DataFrame containing missing values.

        Returns:
        pd.DataFrame: The DataFrame with missing values handled.
        """
        pass
    
    

# Concrete Strategy for Dropping Missing Values
class DropMissingValuesStrategy(MissingValueHandlingStrategy):
    def __init__(self, axis=0, thresh=None):
        """
        Initializes the DropMissingValuesStrategy with specific parameters.

        Parameters:
        axis (int): 0 to drop rows with missing values, 1 to drop columns with missing values.
        thresh (int): The threshold for non-NA values. Rows/Columns with less than thresh non-NA values are dropped.
        """
        
        self.axis = axis
        self.thresh = thresh
        
    
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drops rows or columns with missing values based on the axis and threshold.

        Parameters:
        df (pd.DataFrame): The input DataFrame containing missing values.

        Returns:
        pd.DataFrame: The DataFrame with missing values dropped.
        """
        
        logging.info(f"Dropping missing values with axis: {self.axis} and thresh: {self.thresh}")
        df_cleaned = df.dropna(
            axis= self.axis,
            thresh= self.thresh
        )
        logging.info("Missing values dropped.")
        return df_cleaned
    
    

# Concrete Stratege for Filling Missing values
class FillMissingValuesStrategy(MissingValueHandlingStrategy):
    def __init__(
        self,
        method= "mean",
        fill_value=None
    ):
        """
        Initializes the FillMissingValuesStrategy with a specific method or fill value.

        Parameters:
        method (str): The method to fill missing values ('mean', 'median', 'mode', or 'constant').
        fill_value (any): The constant value to fill missing values when method='constant'.
        """
        
        self.method = method
        self.fill_value = fill_value
        
    
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fills missing values using the specified method or constant value.

        Parameters:
        df (pd.DataFrame): The input DataFrame containing missing values.

        Returns:
        pd.DataFrame: The DataFrame with missing values filled.
        """
        
        df_cleaned = df.copy()
        logging.info(f"Filling missing values using method: {self.method}")

        if self.method == "mean":
            numaric_columns = df_cleaned.select_dtypes(include="number").columns
            df_cleaned[numaric_columns] = df_cleaned[numaric_columns].fillna(
                df[numaric_columns].mean()
            )
            
        elif self.method == "median":
            numaric_columns = df_cleaned.select_dtypes(include="number").columns
            df_cleaned[numaric_columns] = df_cleaned[numaric_columns].fillna(
                df[numaric_columns].median()
            )
            
        elif self.method == "mode":
            numaric_columns = df_cleaned.select_dtypes(include="number").columns
            df_cleaned[numaric_columns] = df_cleaned[numaric_columns].fillna(
                df[numaric_columns].mode()
            )
            
        elif self.method == "constant":
            df_cleaned = df_cleaned.fillna(self.fill_value)
        else:
            logging.warning(f"Unknown method '{self.method}'. No missing values handeled.")
        
        logging.info("Missing values filled.")
        return df_cleaned
    

# Context class for handling Missing Values.
class MissingValueHandler:
    def __init__(self, strategy: MissingValueHandlingStrategy):
        """
        Initializes the MissingValueHandler with a specific missing value handling strategy.

        Parameters:
        strategy (MissingValueHandlingStrategy): The strategy to be used for handling missing values.
        """
        
        self._strategy = strategy
        
    
    def set_strategy(self, strategy: MissingValueHandlingStrategy):
        """
        Sets a new strategy for the MissingValueHandler.

        Parameters:
        strategy (MissingValueHandlingStrategy): The new strategy to be used for handling missing values.
        """
        
        logging.info("Switching missing value handling strategy.")
        self._strategy = strategy
        
        
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the missing value handling using the current strategy.

        Parameters:
        df (pd.DataFrame): The input DataFrame containing missing values.

        Returns:
        pd.DataFrame: The DataFrame with missing values handled.
        """
        
        logging.info("Executing missing value handling strategy.")
        return self._strategy.handle(df)
    
    
    
if __name__ == "__main__":
    ...