import logging 
import os 
from datetime import datetime
from from_root import from_root 
from logging.handlers import RotatingFileHandler

#this is to specify filename and directory it will be in 

LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of backup log files to keep

log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True) #Do nothing if the folder is already there 

log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    
    #Create a custom logger
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    #defining formatter 
    
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")
    
    #File handler along with rotation 
    
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    #Console handler 
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
