from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV = "qa"
DEFAULT_BASE_URL = "https://opensource-demo.orangehrmlive.com"
DEFAULT_APP_PATH = "/web/index.php/auth/login"


def _load_environment_file(environment):
    env_files = [
        PROJECT_ROOT / ".env",
        PROJECT_ROOT / "Utilities" / ".env",
        PROJECT_ROOT / "config" / f"{environment}.env",
    ]
    for env_file in env_files:
        if env_file.exists():
            load_dotenv(env_file, override=True)


RUN_ENV = os.getenv("ENV", DEFAULT_ENV).lower()
_load_environment_file(RUN_ENV)
RAW_BASE_URL = os.getenv("BASE_URL", DEFAULT_BASE_URL).strip()
RAW_APP_PATH = os.getenv("APP_PATH", DEFAULT_APP_PATH).strip()


def _normalise_base_url(url):
    marker = "/web/index.php"
    if marker in url:
        return url.split(marker)[0]
    return url.rstrip("/")


def _normalise_app_path(base_url, app_path):
    marker = "/web/index.php"
    if marker in base_url:
        return f"{marker}{base_url.split(marker, 1)[1]}"
    return app_path


class Config:
    ENV = RUN_ENV
    BASE_URL = _normalise_base_url(RAW_BASE_URL)
    APP_PATH = _normalise_app_path(RAW_BASE_URL, RAW_APP_PATH)
    USERNAME = os.getenv("ORANGEHRM_USERNAME", "Admin").strip()
    PASSWORD = os.getenv("ORANGEHRM_PASSWORD", "admin123").strip()
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    @classmethod
    def app_url(cls):
        return f"{cls.BASE_URL.rstrip('/')}/{cls.APP_PATH.lstrip('/')}"
