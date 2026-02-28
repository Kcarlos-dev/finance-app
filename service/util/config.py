import os
import dotenv

dotenv.load_dotenv()

def get_config(key):
    return os.getenv(key)