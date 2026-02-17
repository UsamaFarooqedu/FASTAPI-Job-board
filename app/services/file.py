import os
import shutil
from fastapi import UploadFile
from datetime import datetime
import uuid

UPLOAD_DIR = "app/static/uploads"
PROFILE_DIR = f"{UPLOAD_DIR}/profiles"
RESUME_DIR = f"{UPLOAD_DIR}/resumes"
JOB_IMG_DIR = f"{UPLOAD_DIR}/job_images"
POST_IMG_DIR = f"{UPLOAD_DIR}/post_images"

def save_upload_file(upload_file: UploadFile, destination_dir: str) -> str:
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
    
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(destination_dir, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    # Return relative path for static serving
    return file_path.replace("app/static/", "/static/")

def save_profile_picture(upload_file: UploadFile) -> str:
    return save_upload_file(upload_file, PROFILE_DIR)

def save_resume(upload_file: UploadFile) -> str:
    return save_upload_file(upload_file, RESUME_DIR)

def save_job_image(upload_file: UploadFile) -> str:
    return save_upload_file(upload_file, JOB_IMG_DIR)

def save_post_image(upload_file: UploadFile) -> str:
    return save_upload_file(upload_file, POST_IMG_DIR)

def delete_file(file_path: str):
    # Convert static URL back to local path
    local_path = file_path.replace("/static/", "app/static/")
    if os.path.exists(local_path):
        os.remove(local_path)
