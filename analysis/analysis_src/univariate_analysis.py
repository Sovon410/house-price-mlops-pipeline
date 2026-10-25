from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Abstract Base Class for Univariate Analysis Strategy
# -----------------------------------------------------
# This class defines a common interface for univariate analysis strategies.
# Subclasses must implement the analyze method.

class UnivariateAlalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, df: pd.DataFrame, faetures: str):
        """
        Perform univariate analysis on a specific feature of the dataframe.

        Parameters:
        df (pd.DataFrame): The dataframe containing the data.
        feature (str): The name of the feature/column to be analyzed.

        Returns:
        None: This method visualizes the distribution of the feature.
        """
        
        pass
    


# Concrete Strategy for Numerical Features
# -----------------------------------------
# This strategy analyzes numerical features by plotting their distribution.

class NumericalUnivariateAnalysis(UnivariateAlalysisStrategy):
    def analyze(self, df: pd.DataFrame, features: str):
        """
        Plots the distribution of a numerical feature using a histogram and KDE.

        Parameters:
        df (pd.DataFrame): The dataframe containing the data.
        feature (str): The name of the numerical feature/column to be analyzed.

        Returns:
        None: Displays a histogram with a KDE plot.
        """
        
        plt.figure(figsize=(10, 8))
        sns.histplot(
            df[features],
            kde=True,
            bins= 45
        )
        plt.title(f"Distribution of {features}")
        plt.xlabel(features)
        plt.ylabel("Freauency")
        plt.show()
        


# Concrete Strategy for Categorical Features
# -------------------------------------------
# This strategy analyzes categorical features by plotting their frequency distribution.

class CategoricalUnivariateAnalysis(UnivariateAlalysisStrategy):
    def analyze(self, df: pd.DataFrame, faetures: str):
        """
        Plots the distribution of a categorical feature using a bar plot.

        Parameters:
        df (pd.DataFrame): The dataframe containing the data.
        feature (str): The name of the categorical feature/column to be analyzed.

        Returns:
        None: Displays a bar plot showing the frequency of each category.
        """
        
        plt.figure(figsize=(10, 8))
        sns.countplot(
            x=faetures,
            data=df,
            palette="muted"
        )
        plt.title(f"Distribution of {faetures}")
        plt.xlabel(faetures)
        plt.ylabel("Count")
        plt.xticks(rotation= 45)
        plt.show()
        
        

# Context Class that uses a UnivariateAnalysisStrategy
# ----------------------------------------------------
# This class allows you to switch between different univariate analysis strategies.

class UnivariateAnalyzer:
    def __init__(self, strategy: UnivariateAlalysisStrategy):
        """
        Initializes the UnivariateAnalyzer with a specific analysis strategy.

        Parameters:
        strategy (UnivariateAnalysisStrategy): The strategy to be used for univariate analysis.

        Returns:
        None
        """
        
        self._strategy = strategy
        
        
    def set_strategy(self, strategy: UnivariateAlalysisStrategy):
        """
        Sets a new strategy for the UnivariateAnalyzer.

        Parameters:
        strategy (UnivariateAnalysisStrategy): The new strategy to be used for univariate analysis.

        Returns:
        None
        """
        
        self._strategy = strategy
        
        
    def execute_analysis(self, df: pd.DataFrame, features: str):
        """
        Executes the univariate analysis using the current strategy.

        Parameters:
        df (pd.DataFrame): The dataframe containing the data.
        feature (str): The name of the feature/column to be analyzed.

        Returns:
        None: Executes the strategy's analysis method and visualizes the results.
        """
        
        self._strategy.analyze(df, features)
        
        

if __name__ == "__main__":
    # # Example usage of the UnivariateAnalyzer with different strategies.

    # # Load the data
    # df = pd.read_csv("extracted_data/AmesHousing.csv")
    
    # # Analyzing a numerical feature
    # analyzer = UnivariateAnalyzer(NumericalUnivariateAnalysis())
    # analyzer.execute_analysis(df, 'SalePrice')

    # # Analyzing a categorical feature
    # analyzer.set_strategy(CategoricalUnivariateAnalysis())
    # analyzer.execute_analysis(df, 'Neighborhood')
    
    ...