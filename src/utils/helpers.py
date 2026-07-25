import time
import os
from functools import wraps
from typing import Any, Callable
import pandas as pd
from src.utils.logger import setup_logger

# Initialize logger for helpers module
logger = setup_logger("helpers")

def time_it(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that measures and logs the execution time of a function.
    Useful for tracking long-running data extractions or cleaning tasks.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        logger.info(f"Starting execution of function '{func.__name__}'...")
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Finished function '{func.__name__}' in {duration:.2f} seconds.")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Function '{func.__name__}' failed after {duration:.2f} seconds with error: {e}")
            raise e
            
    return wrapper

def save_dataframe(df: pd.DataFrame, filepath: str, index: bool = False) -> bool:
    """
    Safely saves a Pandas DataFrame to a CSV file.
    Creates parent directories automatically if they do not exist.
    
    Args:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): Target destination filepath (e.g., 'data/raw/sales.csv').
        index (bool): Whether to write row names (index) to file. Default is False.
        
    Returns:
        bool: True if file was saved successfully, False otherwise.
    """
    try:
        # Check if DataFrame is empty
        if df.empty:
            logger.warning(f"Attempted to save an empty DataFrame to: {filepath}")
            
        # Ensure directories exist
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directories: {directory}")
            
        # Save to CSV
        df.to_csv(filepath, index=index)
        logger.info(f"Successfully saved DataFrame of shape {df.shape} to: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to save DataFrame to {filepath}: {e}")
        return False

def format_large_number(num: float) -> str:
    """
    Formats a large numeric value into a readable string (K, M, B).
    E.g., 1,500,000 -> 1.50M; 2,500 -> 2.50K.
    
    Args:
        num (float): Number to format.
        
    Returns:
        str: Formatted string representation.
    """
    if num is None:
        return "N/A"
        
    abs_num = abs(num)
    sign = "-" if num < 0 else ""
    
    if abs_num >= 1_000_000_000:
        return f"{sign}{abs_num / 1_000_000_000:.2f}B"
    elif abs_num >= 1_000_000:
        return f"{sign}{abs_num / 1_000_000:.2f}M"
    elif abs_num >= 1_000:
        return f"{sign}{abs_num / 1_000:.2f}K"
    else:
        return f"{sign}{abs_num:.2f}"
