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
# import cv2
from fastapi.responses import JSONResponse

from tools.openCV_tool import random_bounding_box
from tools.yolo import Model

from tools.dir_tools import clear_directory
from config.paths import SEGMENTATION_PATH,UPLOADS_PATH

model = Model()
router = APIRouter()

@router.post("/single", status_code=201)
async def upload_image(file= File(...)):
    uuid_val = uuid.uuid4()
    upload_dir = f"uploads/uploads_{uuid_val}"
    os.makedirs(upload_dir, exist_ok=True)
    file_name = file.filename
    file = await file.read()
    image = Image.open(io.BytesIO(file))
    file_path = os.path.join(upload_dir, file_name)
    image.save(file_path)
    model.segment(input_dir=upload_dir)
    with open(f"segmentation/{uuid_val}/{file_name}", 'rb') as text_file:
        text_binary = text_file.read()
    with open(f"segmentation/{uuid_val}/labels/{'.'.join(file_name.split('.')[:-1])}.txt", 'rb') as text_file:
        label = text_file.read()
    return JSONResponse(content={"uploadStatus": "complete", "image": base64.b64encode(text_binary).decode('utf-8'),"labels":[base64.b64encode(label).decode('utf-8')]},status_code=201)
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