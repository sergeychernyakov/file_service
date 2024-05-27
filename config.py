import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    PORT = int(os.getenv('PORT', 5002))
    STORAGE_PATH = os.getenv('STORAGE_PATH', './storage')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 1048576))
    USERNAME = os.getenv('USERNAME', 'admin')
    PASSWORD = os.getenv('PASSWORD', 'password')
