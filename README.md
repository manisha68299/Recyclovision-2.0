♻️ RecycloVision  
AI-Powered Smart Waste Segregation & Sustainability Analytics System  
RecycloVision is a Real-Time AI Waste Detection & Sustainability Intelligence System developed using YOLOv8, OpenCV, SQLite, and Streamlit.

### 🚀 Key Features
### 🎯 Real-Time AI Detection  
YOLOv8  
Live Camera Feed  
Confidence Score  
Bounding Box  

### 🗑 Smart Bin Validation  
Dynamic Bin Selection  
Real-Time Contamination Detection  
Contamination Prevention Tracking  

### 📊 Campus Purity Score  
Calculation of Segregation Accuracy  
Formula  
"Correct Detections/Total Detections * 100"  
Live Purity Calculation Display on Video Feed  

### 🌱 Carbon Impact Estimator  
Tracking of CO2 Savings Per Recyclable Item  
Live Cumulative Carbon Savings  
Sustainability Intelligence Calculations  

### 🧠 Performance Monitoring  
Real-Time FPS Calculation  
Inference Latency  
System Performance Monitoring  

### 🗄 Production-Ready Database  
SQLite  
Fast Query Response using Indexed Tables  
Detection Logs  
Carbon Savings Logs  
Low Confidence Detection  

### 📈 Interactive Dashboard  
Streamlit  
Total Detections  
Average Confidence  
Purity Trend Graph  
Waste Type  
Low Confidence  
Sustainability  

## 🧪 How It Works  
1. Captures Video Frames  
2. Object Detection using YOLO  
3. Bin Validation Logic  
4. Purity Calculation  
5. Carbon Savings Calculation  
6. Logs Data to SQLite  
7. Displays Live Metrics on Video Feed  
8. Live Dashboard Display

## 🏗 Project Architecture

recyclovision/
│
├── ai/
│ └── detector.py
│
├── logic/
│ ├── tracker.py
│ ├── carbon.py
│ └── rules.py
│
├── vision/
│ ├── camera.py
│ ├── hud.py
│ ├── lighting.py
│ └── performance.py
│
├── database/
│ └── db_manager.py
│
├── dashboard/
│ └── ui.py
│
├── data/
│ └── waste_telemetry.db
│
├── logs/
│ └── database.log
│
├── main.py
└── requirements.txt

