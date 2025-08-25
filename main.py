
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import uuid
import os
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ant - Simple Image Resizer")

UPLOAD_DIR = "uploads"
# Clean up uploads directory for debugging
if os.path.exists(UPLOAD_DIR):
    shutil.rmtree(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/resize/")
async def resize_image(
    file: UploadFile,
    width: int = Form(...),
    height: int = Form(...)
):
    try:
        logger.info(f"Resizing image: {file.filename}, width: {width}, height: {height}")

        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Open and resize with Pillow
        image = Image.open(file.file)
        resized = image.resize((width, height))
        resized.save(filepath)

        logger.info(f"Image resized and saved to {filepath}")
        return FileResponse(filepath, media_type="image/png", filename=filename)
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        return {"error": "Failed to resize image."}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

