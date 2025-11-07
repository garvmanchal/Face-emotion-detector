import face_recognition
import cv2
import numpy as np
import csv
import pyttsx3
import random
from deepface import DeepFace
from datetime import datetime

# ======= Camera Setup =======
# url = "http://100.112.31.:8080/video"  # For phone camera
# video_capture = cv2.VideoCapture(url)
video_capture = cv2.VideoCapture(0)  # For laptop camera

# ======= Load Known Faces =======
people = {

    "Garv": "grv.jpeg",
    "Aashi": "aashi.jpeg",
    "Raj": "raj.jpeg",
    "Sanjay": "sanjay.jpeg",
    "Sudhanshu": "sudhanshu.jpeg",
    "Sahil": "sahil.jpeg"

}

known_face_encodings = []
known_face_names = []

for name, file in people.items():
    try:
        img = face_recognition.load_image_file(file)
        enc = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(enc)
        known_face_names.append(name)
        print(f"✅ Loaded {name}'s face successfully.")
    except Exception as e:
        print(f"⚠️ Could not load {name}'s image: {e}")

students = known_face_names.copy()

# ======= CSV Setup =======
current_date = datetime.now().strftime("%Y-%m-%d")
f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)
lnwriter.writerow(["Name", "Time"])

# ======= Voice Engine Setup =======
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# ======= Helper Functions =======
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 16:
        return "Good Afternoon"
    elif 16 <= hour < 21:
        return "Good Evening"
    else:
        return "Hello"

def speak_line(line):
    engine.say(line)
    engine.runAndWait()

def emotion_comment(emotion):
    if emotion == "happy":
        return "You look really happy today!"
    elif emotion == "sad":
        return "Don't worry buddy, everything will be okay."
    elif emotion == "neutral":
        return "You seem calm and focused today."
    else:
        return f"You seem {emotion} today."

# ======= Colors for Boxes =======
colors = [(0, 255, 0), (255, 0, 0), (0, 128, 255), (255, 128, 0), (255, 0, 255)]

# ======= Main Loop =======
while True:
    ret, frame = video_capture.read()

    if not ret:
        print("⚠️ Frame not received. Retrying...")
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        name = "Unknown"
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # ======= Emotion Detection =======
        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            dominant_emotion = result[0]["dominant_emotion"]
        except:
            dominant_emotion = "neutral"

        # Scale coordinates back to original frame
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # ======= Draw Rectangle & Labels =======
        color = random.choice(colors)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, f"{name} ({dominant_emotion})", (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # ======= Attendance Logic =======
        if name != "Unknown" and name in students:
            students.remove(name)
            current_time = datetime.now().strftime("%H:%M:%S")
            lnwriter.writerow([name, current_time])
            print(f"✅ {name} marked present at {current_time}")

            greeting = get_greeting()
            line = random.choice([
                f"{greeting} {name}, great to see you!",
                f"{greeting} {name}, your attendance is marked!",
                f"{greeting} {name}, have a wonderful day!"
            ])
            emotion_line = emotion_comment(dominant_emotion)

            speak_line(f"{line} {emotion_line}")

        elif name == "Unknown":
            stranger_line = f"⚠️ Stranger detected! They seem {dominant_emotion}."
            print(stranger_line)
            speak_line(f"Warning! Unknown person detected. They look {dominant_emotion}.")

    # ======= UI Overlay =======
    cv2.putText(frame, "Press 'Q' to Quit", (10, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("🎥 Smart Face Recognition + Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ======= Cleanup =======
video_capture.release()
cv2.destroyAllWindows()
f.close()

