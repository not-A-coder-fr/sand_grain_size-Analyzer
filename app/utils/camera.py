import cv2
import config

def capture_image(filepath):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        cv2.imwrite(filepath, frame)
        return True
    else:
        return False