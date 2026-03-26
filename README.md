AI Face Emotion & Attendance System (Full Stack + FastAPI)
🚀 Overview

This project is a Full-Stack AI-based Face Recognition & Emotion Detection System powered by FastAPI backend and Computer Vision models.
It captures real-time images via webcam, identifies the person, detects their emotion, and logs attendance automatically.

🧠 Backend Intelligence (Core Highlight 🔥)

Your backend is built using FastAPI and integrates:

Face Recognition (identity detection)
Emotion Analysis (DeepFace model)
Attendance Logging (CSV system)
Real-time camera capture

🔥 Key Features
🎥 Real-time face capture via webcam
🧠 Emotion detection using DeepFace
🧑‍💻 Face recognition using encodings
📊 Automatic attendance logging (CSV)
⚡ Fast API endpoints using FastAPI
🌐 CORS enabled for frontend integration

🛠️ Tech Stack
Layer	Technology
Backend	FastAPI
AI / ML	DeepFace, face_recognition
Computer Vision	OpenCV
Data Handling	NumPy, CSV
Runtime	Python

📂 Project Structure
Face-emotion-detector/
│── backend/
│   ├── main.py              # FastAPI server
│   ├── images/              # Known faces
│
│── frontend/                # UI
│── face_reco/               # AI logic
│── attendance_*.csv         # Logs
│── package.json             # Node setup

⚙️ Installation & Setup
1️⃣ Clone Repo
git clone https://github.com/garvmanchal/Face-emotion-detector.git
cd Face-emotion-detector
2️⃣ Install Python Dependencies
pip install -r requirements.txt
3️⃣ Run Backend (FastAPI)
uvicorn main:app --reload

👉 Server runs at:

http://127.0.0.1:8000
▶️ API Endpoints
🏠 Home
GET /

✔️ Check if backend is running

🧑‍💻 Recognize Face + Emotion
GET /recognize

Returns:

{
  "user": "Garv",
  "emotion": "happy",
  "timestamp": "14:32:10"
}
🧪 Test Emotion Detection
GET /test-emotion

✔️ Debug endpoint to verify emotion model

🧠 How It Works (Actual Flow)
Camera → Face Detection → Face Encoding → Identity Match → Emotion Detection → CSV Logging → API Response
Webcam captures frame
Face detected using OpenCV
Encodings matched with stored faces
Emotion detected using DeepFace
Data stored in CSV
API sends response
😃 Emotion Detection Logic (Advanced 🔥)

Instead of raw output, system:

Filters only Happy, Sad, Neutral
Chooses highest probability
Returns optimized result

👉 This improves accuracy & stability

📊 Attendance System
Auto-generated CSV file:
attendance_YYYY-MM-DD.csv
Stores:
Name
Emotion
Time

🚧 Future Improvements
📊 Database (MongoDB/MySQL)
🌐 Deploy backend (Render / AWS)
📱 Mobile/Web App integration
📈 Analytics dashboard

👨‍💻 Author:

Garv Manchal
BTech CSE | Python/Backend Developer | FastAPIs | AI Developer

⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
🚀 Share it
🧠 Vision

"Building intelligent systems that understand humans — not just commands."
