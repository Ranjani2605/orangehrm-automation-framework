import os
from dataclasses import dataclass

class Config:
    Base_url : str = os.getenv('BASE_URL', "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    Admin_user : str = os.getenv('ADMIN_USER', os.getenv('ORANGEHRM_USERNAME', "admin"))
    Admin_password : str = os.getenv('ADMIN_PASSWORD', os.getenv('ORANGEHRM_PASSWORD', "admin123"))
    timeout : int = int(os.getenv('TIMEOUT', "10"))

config = Config()

