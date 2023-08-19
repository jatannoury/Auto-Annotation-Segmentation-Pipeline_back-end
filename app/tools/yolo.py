import uuid
import os

from PIL import Image

from ultralytics import YOLO

import ultralytics as ul


class Model:
  def __init__(self, version='yolov8x-seg.pt'):
    self.model = YOLO(version)
    self.output_dir = "./results"

  def resize(self,input_dir, output_dir, size=(500, 300)):
      images = [
          [file_name, Image.open(os.path.join(input_dir, file_name)).resize(size)] \
          for file_name in os.listdir(input_dir)
      ]

      os.makedirs(output_dir, exist_ok=True)
      for image in images:
          image[1].save(os.path.join(output_dir, image[0]))
  def segment(self,input_dir):
      input_dir = input_dir
      uuid_val=input_dir.split("_")[1]
      resized_dir = f"./data/resized_images/{uuid_val}"
      self.resize(input_dir, resized_dir)
      self.model([os.path.join(resized_dir, file_name) \
                          for file_name in os.listdir(resized_dir)],
                         save=True,
                         save_txt=True,
                        project="segmentation",
                        name=uuid_val
                        )

      return resized_dir


