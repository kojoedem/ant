
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from PIL import Image
import uuid
import os

app = FastAPI(title="Ant - Simple Image Resizer")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/resize/")
async def resize_image(
    file: UploadFile,
    width: int = Form(...),
    height: int = Form(...)
):
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Open and resize with Pillow
    image = Image.open(file.file)
    resized = image.resize((width, height))
    resized.save(filepath)

    return FileResponse(filepath, media_type="image/png", filename=filename)

