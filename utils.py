from ultralytics import YOLO
import os
import time
import uuid
import math 
import cv2
from werkzeug.utils import secure_filename
import numpy as np
import base64
from collections import Counter
from flask import Flask, jsonify
from PIL import Image
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
def save_uploaded_file(file, folder):
    input_path = os.path.join(folder, file.filename)
    file.save(input_path)
    return input_path

def make_output_path(filename, folder, prefix='processed'):
    filename_wo_ext, ext = os.path.splitext(filename)
    output_filename = f"{prefix}_{timestamp}_{filename_wo_ext}{ext}"
    output_path = os.path.join(folder, output_filename)
    return output_path, output_filename

def image_detect(file,UPLOAD_FOLDER,RESULT_FOLDER,model):
    input_path = save_uploaded_file(file, UPLOAD_FOLDER)
    output_path, output_filename = make_output_path(file.filename, RESULT_FOLDER)

    results = model(input_path)
    img = results[0].plot()
    cv2.imwrite(output_path, img)
    return output_filename


def video_detect(file, UPLOAD_FOLDER, RESULT_FOLDER, model):
    unique_id = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    temp_video_name = f"temp_video_{unique_id}.mp4"
    result_video_name = f"result_video_{unique_id}.mp4"
    
    temp_video_path = os.path.join(UPLOAD_FOLDER, temp_video_name)
    file.save(temp_video_path)
    
    cap = cv2.VideoCapture(temp_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 30 
    
    result_video_path = os.path.join(RESULT_FOLDER, result_video_name)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(result_video_path, fourcc, fps, (frame_width, frame_height))
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        results = model(frame)
        annotated_frame = results[0].plot() 
        out.write(annotated_frame)
    
    cap.release()
    out.release()
    
    video_url = f"/static/results/{result_video_name}"
    return video_url