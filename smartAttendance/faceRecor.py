import cv2
import os
from datetime import datetime
from deepface import DeepFace
import numpy as np
from io import BytesIO


def verify_user(live_image, logged_in_user_image_path):
    image_bytes = live_image.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    try:
        result = DeepFace.verify(logged_in_user_image_path, image, enforce_detection=False)
        print(result)
        return result

    except:
        return "failed to detect"


def detect_face(image):
    try:
        image_bytes = image.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        faces = DeepFace.extract_faces(image)
        return faces

    except:
        print('no face detected')
        return None