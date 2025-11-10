from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import cv2
import numpy as np
from deepface import DeepFace
from datetime import datetime
import csv
import os

app = FastAPI()


# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load Emotion Model
print("⚙️ Loading emotion model...")
emotion_model = DeepFace.build_model("Emotion")
print("✅ Emotion model loaded successfully!")


# Load Known Faces
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
people = {
    "Garv": "grv.jpeg",
    "Aashi": "aashi.jpeg",
    "Raj": "raj.jpeg",
    "Sanjay": "sanjay.jpeg",
    "Sudhanshu": "sudhanshu.jpeg",
    "Sahil": "sahil.jpeg",
}

known_face_encodings = []
known_face_names = []

for name, file in people.items():
    try:
        path = os.path.join(BASE_DIR, file)
        img = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)
        print(f"✅ Loaded {name}'s face.")
    except Exception as e:
        print(f"⚠️ Could not load {name}: {e}")


# CSV Setup
csv_filename = f"attendance_{datetime.now().strftime('%Y-%m-%d')}.csv"
if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Emotion", "Confidence", "Time"])


# ✨ IMPROVED EMOTION DETECTION FUNCTION ✨
def detect_emotion(face_img, face_location=None):
    """
    Improved emotion detection that properly detects happy, sad, neutral
    """
    try:
        # If face location is provided, crop the face
        if face_location:
            top, right, bottom, left = face_location
            face_crop = face_img[top:bottom, left:right]
        else:
            face_crop = face_img
        
        # Ensure the face crop is valid
        if face_crop.size == 0:
            return "neutral", 0.0
        
        # Analyze emotion with DeepFace
        result = DeepFace.analyze(
            face_crop,
            actions=["emotion"],
            enforce_detection=False,  # Don't fail if face detection fails
            detector_backend="opencv",  # Use opencv for faster detection
            silent=True  # Suppress warnings
        )
        
        # Get emotion probabilities
        if isinstance(result, list):
            result = result[0]
        
        emotions = result["emotion"]
        dominant_emotion = result["dominant_emotion"]
        
        print(f"🎭 All emotions detected: {emotions}")
        print(f"🎯 Dominant emotion: {dominant_emotion}")
        
        # Only focus on 3 emotions: happy, sad, neutral
        happy_score = emotions.get("happy", 0)
        sad_score = emotions.get("sad", 0)
        neutral_score = emotions.get("neutral", 0)
        
        # Find the highest among the 3 target emotions
        target_emotions = {
            "happy": happy_score,
            "sad": sad_score,
            "neutral": neutral_score
        }
        
        final_emotion = max(target_emotions, key=target_emotions.get)
        final_confidence = target_emotions[final_emotion]
        
        print(f"✅ Final emotion: {final_emotion} ({final_confidence:.2f}%)")
        
        return final_emotion, final_confidence
        
    except Exception as e:
        print(f"⚠️ Emotion detection error: {e}")
        return "neutral", 0.0


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.get("/")
def home():
    return {"message": "Backend working fine ✅"}


@app.get("/recognize")
def recognize():
    # Open camera
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return {"user": "Camera Error", "emotion": "N/A", "confidence": 0}

    # Capture frame
    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        return {"user": "Frame Error", "emotion": "N/A", "confidence": 0}

    # Detect faces
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        return {"user": "No face detected", "emotion": "N/A", "confidence": 0}

    # Process first detected face
    face_encoding = face_encodings[0]
    face_location = face_locations[0]
    
    name = "Unknown"
    if known_face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        if len(face_distance) > 0:
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

    # Detect emotion using improved function
    emotion, confidence = detect_emotion(frame, face_location)

    # Save to CSV
    with open(csv_filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, emotion, f"{confidence:.2f}%", datetime.now().strftime("%H:%M:%S")])

    return {
        "user": name, 
        "emotion": emotion,
        "confidence": f"{confidence:.2f}%",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }


@app.get("/test-emotion")
def test_emotion():
    """
    Test endpoint to verify emotion detection is working
    """
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return {"error": "Camera not accessible"}
    
    ret, frame = video_capture.read()
    video_capture.release()
    
    if not ret:
        return {"error": "Could not capture frame"}
    
    # Detect face
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    
    if not face_locations:
        return {"error": "No face detected"}
    
    face_location = face_locations[0]
    emotion, confidence = detect_emotion(frame, face_location)
    
    return {
        "emotion": emotion,
        "confidence": f"{confidence:.2f}%",
        "status": "Emotion detection working! ✅"
    }