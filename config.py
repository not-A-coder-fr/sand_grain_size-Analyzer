import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")
RESULT_FILE = os.path.join(BASE_DIR, "data", "results.csv")

CAMERA_WIDTH = 4056
CAMERA_HEIGHT = 3040
CAMERA_FOV_H = 62.2 * (3.14159 / 180)  # radians

TOF_ADDRESS = 0x29
GNSS_PORT = "/dev/ttyAMA0"
GNSS_BAUD = 9600

HOST = "0.0.0.0"
PORT = 5000

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)