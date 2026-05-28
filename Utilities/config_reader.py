import os
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parent
env_path = project_root / ".env"
load_dotenv(env_path, override=True)


class Config:
    BASE_URL = os.getenv("BASE_URL")
    USERNAME = os.getenv("ORANGEHRM_USERNAME")
    PASSWORD = os.getenv("ORANGEHRM_PASSWORD")



