# ♻️ RecycloVision  
AI-Powered Smart Waste Segregation & Sustainability Intelligence System  

📦 GitHub: https://github.com/manisha68299/Recyclovision-2.0  

---

## Problem  

Waste segregation is still manual, error-prone, and lacks real-time monitoring. This leads to contamination of recyclable waste, inefficient disposal, and no measurement of environmental impact. There is no system that combines AI-based detection, validation, and analytics into one intelligent solution.

---

## Solution  

RecycloVision is a real-time AI system that detects waste using YOLOv8, validates correct disposal into bins, calculates segregation accuracy (Purity Score), tracks carbon savings, and displays live analytics through a web-based dashboard.

---

## Features  

- Real-time waste detection using YOLOv8  
- Browser-based webcam access using WebRTC  
- Bounding boxes with confidence scores  
- Smart bin validation (Recyclable / General / E-Waste)  
- Contamination detection system  
- Purity Score calculation  

Purity = (Correct Detections / Total Detections) × 100  

- Carbon impact tracking (CO₂ savings per item)  
- Live dashboard with metrics and insights  
- Performance monitoring (FPS, latency)  
- SQLite-based logging system  

---

## Tech Stack  

- AI / ML: YOLOv8 (Ultralytics), OpenCV  
- Frontend: Streamlit  
- Streaming: streamlit-webrtc (WebRTC)  
- Backend: Python  
- Database: SQLite  
- Libraries: NumPy, Pandas  

---

## Architecture  

User (Browser Camera)  
→ Streamlit Web App  
→ YOLOv8 Detection  
→ Validation Logic  
→ Carbon Tracking  
→ SQLite Database  
→ Live Dashboard  

---

## Project Structure  

RecycloVision/  
│  
├── app.py                # Cloud deployed app (Streamlit + WebRTC)  
├── main.py               # Local system (OpenCV + camera)  
│  
├── ai/  
│   └── detector.py       # YOLO detection wrapper  
│  
├── logic/  
│   ├── tracker.py        # Purity score calculation  
│   ├── carbon.py         # Carbon impact tracking  
│   └── rules.py          # Waste validation system  
│  
├── vision/  
│   ├── camera.py         # Camera handling  
│   ├── hud.py            # Overlay display  
│   ├── lighting.py       # Frame quality detection  
│   └── performance.py    # FPS and latency  
│  
├── database/  
│   └── db_manager.py     # SQLite management  
│  
├── data/  
│   └── waste_telemetry.db  
│  
├── model/  
│   └── best.pt           # Trained YOLO model  
│  
├── requirements.txt  
└── README.md  

---

## How It Works  

1. User opens the web application  
2. Browser requests webcam access  
3. Video frames are processed using YOLOv8  
4. Objects are detected and classified  
5. System validates correct bin usage  
6. Purity score is calculated  
7. Carbon savings are updated  
8. Data is stored in SQLite database  
9. Dashboard updates in real-time  

---

## Deployment  

The system is deployed using Streamlit Cloud.  
Webcam access is handled through WebRTC, allowing real-time AI detection directly in the browser without local dependencies.  

---

## Installation  

git clone https://github.com/manisha68299/Recyclovision-2.0.git  
cd Recyclovision-2.0  
pip install -r requirements.txt  

Run locally (OpenCV version):  
python main.py  

Run web app (Streamlit version):  
streamlit run app.py  

---

## Future Improvements  

- Edge deployment (Raspberry Pi / Jetson Nano)  
- Cloud database integration  
- Mobile application support  
- Improved model accuracy  

---

## Conclusion  

RecycloVision is a complete AI-driven waste management system that combines computer vision, real-time analytics, and sustainability tracking to solve a real-world environmental problem.