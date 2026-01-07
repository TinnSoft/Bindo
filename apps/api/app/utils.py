import os
from uuid import uuid4
from .config import UPLOAD_DIR, ensure_upload_dir

ensure_upload_dir()

def save_upload_file(upload_file) -> str:
    # Save UploadFile to UPLOAD_DIR and return absolute path
    filename = f"{uuid4().hex}_{upload_file.filename}"
    dest_path = os.path.join(UPLOAD_DIR, filename)
    with open(dest_path, 'wb') as f:
        for chunk in upload_file.file:
            f.write(chunk)
    return dest_path
