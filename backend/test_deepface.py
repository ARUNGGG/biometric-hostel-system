import cv2
import numpy as np
from deepface import DeepFace

img = np.zeros((300, 300, 3), dtype=np.uint8)
try:
    print("Testing FaceNet + SSD allocation...")
    res = DeepFace.represent(img_path=img, model_name="Facenet", enforce_detection=False, detector_backend="ssd")
    print("SUCCESS: AI loaded completely and mathematically parsed the frame!")
except Exception as e:
    print(f"CRASH: {e}")
