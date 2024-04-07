import logging
import os

def get_logger_object(filename: str,log_folder:str, log_filename: str):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    os.makedirs(os.path.join(log_folder), exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_folder, log_filename + ".log"))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
