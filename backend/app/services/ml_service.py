from deepface import DeepFace
import base64
import cv2
import numpy as np
from typing import List

def get_embedding(image_base64: str) -> List[float]:
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]
    
    img_data = base64.b64decode(image_base64)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Natively enforces actual face bounds
    embedding_obj = DeepFace.represent(img_path=img, model_name="Facenet", enforce_detection=True, detector_backend="ssd")
    return embedding_obj[0]["embedding"]

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def is_match(embedding1: List[float], embedding2: List[float], threshold: float = 0.85) -> tuple[bool, float]:
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity > threshold, similarity
