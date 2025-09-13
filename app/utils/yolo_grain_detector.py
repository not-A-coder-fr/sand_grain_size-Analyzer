from ultralytics import YOLO
import config

model = YOLO(config.MODEL_PATH)

def detect_grains(image_path):
    results = model(image_path, conf=0.3, iou=0.45, verbose=False)
    return results[0]