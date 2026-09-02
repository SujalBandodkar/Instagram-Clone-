import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def save_file(file, prefix, user_id):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None
    filename = secure_filename(file.filename)
    filename = f"{prefix}_{user_id}_{datetime.now().timestamp()}_{filename}"
    try:
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    except Exception:
        return None
    return filename
