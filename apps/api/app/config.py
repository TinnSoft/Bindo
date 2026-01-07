import os

DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/data/uploads')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def ensure_upload_dir():
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    except Exception:
        pass
