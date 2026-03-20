import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent
    INSTANCE_DIR = BASE_DIR / "instance"
    DATABASE = INSTANCE_DIR / "truthlens.db"
    MODEL_PATH = BASE_DIR / "ml" / "model.pkl"
    SECRET_KEY = os.environ.get("SECRET_KEY", "truthlens-change-me")
    JSON_SORT_KEYS = False
    MAX_INPUT_CHARS = 10000
    REQUEST_TIMEOUT_SECONDS = 8
