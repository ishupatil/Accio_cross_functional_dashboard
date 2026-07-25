import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "retailmart", log_file: str = "reports/project.log", level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger instance with console and file handlers.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Filepath where logs should be written.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        
    Returns:
        logging.Logger: Configured logger object.
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # If logger is already configured, don't add handlers again
    if logger.handlers:
        return logger
        
    logger.setLevel(level)
    
    # Create formatters
    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 1. Console Handler (Outputs to terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # Ensure directories for the log file exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        
    # 2. File Handler (Saves to a file, rolls over at 5MB, keeps 3 backups)
    try:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not initialize file logging: {e}. Logging to console only.")
        
    return logger
