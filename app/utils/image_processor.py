import cv2
import numpy as np
import csv
import os
import config
from datetime import datetime

def process_image_and_save_results(image_path, tof_distance_m, lat, lon):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    real_world_width = 2 * tof_distance_m * np.tan(config.CAMERA_FOV_H / 2)
    px_per_mm = w / real_world_width

    results = detect_grains(image_path)
    grain_sizes_mm = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        roi = img[y1:y2, x1:x2]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area_px = cv2.contourArea(cnt)
            area_mm2 = area_px / (px_per_mm ** 2)
            grain_sizes_mm.append(np.sqrt(area_mm2))

    count = len(grain_sizes_mm)
    avg_size = np.mean(grain_sizes_mm) if grain_sizes_mm else 0
    std_dev = np.std(grain_sizes_mm) if grain_sizes_mm else 0

    timestamp = datetime.now().isoformat()
    filename = os.path.basename(image_path)
    row = [filename, count, avg_size, std_dev, lat, lon, timestamp]

    with open(config.RESULT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["image_name", "grain_count", "avg_size_mm", "std_dev_mm", "lat", "lon", "timestamp"])
        writer.writerow(row)

    # Annotate and save
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{box.conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    annotated_path = image_path.replace(".jpg", "_annotated.jpg")
    cv2.imwrite(annotated_path, img)

    return {
        "count": count,
        "avg_size_mm": round(avg_size, 3),
        "std_dev_mm": round(std_dev, 3),
        "image_annotated": annotated_path.replace("/data/images/", "/images/")
    }