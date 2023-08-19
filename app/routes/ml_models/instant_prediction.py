import base64
import datetime
import os
import shutil
import uuid
from typing import List, Dict

import numpy as np
from PIL import Image
import io
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
import cv2
from fastapi.responses import JSONResponse

from tools.openCV_tool import random_bounding_box
from tools.yolo import Model

from tools.dir_tools import clear_directory
from config.paths import SEGMENTATION_PATH,UPLOADS_PATH

model = Model()
router = APIRouter()

@router.post("/single", status_code=201)
async def upload_image(file:bytes= File(...)):
    allowed_extensions = [".jpeg", ".png", ".jpg",".avif"]
    image = Image.open(io.BytesIO(file))
    image = np.array(image)  # Convert PIL Image to numpy array
    image_with_bbox = random_bounding_box(image)
    for extension in allowed_extensions:
        try:
            _, buffer = cv2.imencode(extension, cv2.cvtColor(image_with_bbox, cv2.COLOR_RGB2BGR))
        except:
            continue

    # Encode the bytes as base64
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    return JSONResponse(content={"uploadStatus": "complete", "image": image_base64},status_code=201)
def is_valid_image(file) -> bool:
    try:
        Image.open(file)
        return True
    except:
        return False


@router.post("/batch", status_code=201)
async def upload_multiple_images(file_uploads: List[UploadFile]):
    uuid_val = uuid.uuid4()
    upload_dir = f"uploads/uploads_{uuid_val}"
    os.makedirs(upload_dir, exist_ok=True)

    allowed_extensions = [".jpeg", ".png", ".jpg", ".avif"]
    response = []
    for file in file_uploads:
        file_name = file.filename
        file = await file.read()
        image = Image.open(io.BytesIO(file))
        file_path = os.path.join(upload_dir, file_name)
        image.save(file_path)


    results = model.segment(input_dir=upload_dir)
    b64_results = []
    labels=[]
    generated_files = list(os.listdir(os.path.join(SEGMENTATION_PATH,str(uuid_val))))
    generated_files.remove("labels")
    for file in generated_files:
        with open(os.path.join(SEGMENTATION_PATH,str(uuid_val),file), 'rb') as image_file:
            image_binary = image_file.read()
            b64_results.append(base64.b64encode(image_binary).decode('utf-8'))
    for file in os.listdir(os.path.join(SEGMENTATION_PATH,str(uuid_val),"labels")):
        with open(os.path.join(SEGMENTATION_PATH,str(uuid_val),"labels",file), 'rb') as text_file:
            text_binary = text_file.read()
            labels.append(base64.b64encode(text_binary).decode('utf-8'))
    clear_directory(SEGMENTATION_PATH)
    clear_directory(UPLOADS_PATH)
    return JSONResponse(content={"uploadStatus": "complete", "images": b64_results,"labels":labels}, status_code=201)