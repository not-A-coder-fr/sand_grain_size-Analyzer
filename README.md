

# 🏖️ **Sand Grain Size Analyzer (Field-Ready AI System)**

**An offline, AI-powered sand grain analysis system for coastal studies and environmental monitoring**, built on Raspberry Pi 5 with YOLOv8 object detection, OpenCV image processing, and real-time geotagging.

---

## 🚀 **Key Features**
- **AI Grain Detection**: Uses YOLOv8n for fast, accurate sand grain identification
- **Size Calibration**: Integrates VL53L1X ToF sensor for pixel-to-millimeter conversion
- **Geospatial Data**: u-blox NEO-M8N GNSS module for latitude/longitude tagging
- **Offline Operation**: Runs entirely on Raspberry Pi without internet
- **Touchscreen UI**: Responsive web interface for field use
- **Data Export**: CSV output for grain count, size distribution, and metadata

---

## 🔧 **Technologies Used**
| Hardware | Software |
|----------|----------|
| Raspberry Pi 5 (8GB) | Python, Flask, YOLOv8 |
| Pi Camera v3 (12MP) | OpenCV, Pillow |
| VL53L1X ToF Sensor | smbus2, pynmea2 |
| u-blox NEO-M8N GNSS | Bootstrap, JavaScript |
| 7" HDMI Touchscreen | systemd service |

---

## 📊 **How It Works**
1. Capture high-res images of sand samples using Pi Camera
2. YOLO detects individual grains and calculates size using TOF calibration
3. GNSS tags location data in real time
4. Results displayed on touchscreen with CSV export

---

## 🌍 **Deployment**
```bash
# Clone repo
git clone https://github.com/yourusername/sand-grain-analyzer.git

# Install dependencies
pip3 install -r requirements.txt

# Run app
python3 main.py
```
---

## 🌟 **Why This Matters**
- **Coastal Studies**: Quantifies beach erosion patterns
- **Environmental Monitoring**: Tracks sediment changes over time
- **Education**: Field-deployable teaching tool for geoscience

---

## 🛠️ **Future Improvements**
- Bluetooth printing for instant field reports
- Solar-powered battery pack for extended deployments
- Cloud sync for remote data access

---

This description emphasizes:
- **Technical rigor** (YOLOv8, ToF calibration)
- **Practical application** (coastal studies, environmental monitoring)
- **Hackathon readiness** (offline deployment, field-tested design)
- **Scalability** (future improvements section)

---

### 📁 **Core Files**
| File | Purpose |
|------|---------|
| **`main.py`** | Project entry point. Starts Flask server when run. |
| **`config.py`** | Central configuration (paths, sensor settings, camera specs). |
| **`requirements.txt`** | Lists Python dependencies (Flask, OpenCV, YOLO, etc.). |

---

### 🌐 **Web Interface**
| File | Purpose |
|------|---------|
| **`static/styles.css`** | UI styling (dark mode, responsive layout, colors). |
| **`static/script.js`** | Frontend logic (camera capture, data processing, CSV export). |
| **`templates/index.html`** | Main UI page (camera preview, capture button, analysis results). |
| **`templates/results.html`** | Dedicated results page (geotagged data, processed image). |

---

### 🤖 **AI & Processing**
| File | Purpose |
|------|---------|
| **`models/best.pt`** | Pre-trained YOLOv8 model (detects sand grains). |
| **`app/routes.py`** | Handles API endpoints (image capture, analysis, data export). |
| **`app/utils/image_processor.py`** | Processes images: calculates grain size using ToF calibration. |
| **`app/utils/yolo_grain_detector.py`** | Runs YOLO model on captured images. |

---

### 📡 **Hardware Integration**
| File | Purpose |
|------|---------|
| **`app/utils/camera.py`** | Captures images from Pi Camera (or laptop webcam). |
| **`app/utils/tof_calibrate.py`** | Reads VL53L1X ToF sensor for pixel-to-mm calibration. |
| **`app/utils/gnss_parser.py`** | Parses u-blox NEO-M8N GNSS data for geotagging. |

---

### 🚀 **Deployment Files**
| File | Purpose |
|------|---------|
| **`scripts/start_service.sh`** | Script to launch the app (used by systemd service). |
| **`systemd/sand-analyzer.service`** | Configures auto-start on Raspberry Pi boot. |
| **`data/images/`** | Stores captured sand grain images. |
| **`data/results.csv`** | Logs analysis results (grain count, size, location, timestamp). |


