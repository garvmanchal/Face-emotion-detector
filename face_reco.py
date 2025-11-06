import face_recognition
import cv2
import numpy as np 
import csv
import pyttsx3
import random
from deepface import DeepFace
from datetime import datetime

# url = "http://100.112.31.:8080/video"   #  for phone connection
# video_capture = cv2.VideoCapture(url)
video_capture = cv2.VideoCapture(0) # for laptop camera


# Loading known faces
garv_image = face_recognition.load_image_file("garv1.jpeg")
garv_encoding = face_recognition.face_encodings(garv_image)[0] 

aashi_image = face_recognition.load_image_file("aashi1.jpeg")
aashi_encoding = face_recognition.face_encodings(aashi_image)[0]

raj_image = face_recognition.load_image_file("raj1.jpeg")
raj_encoding = face_recognition.face_encodings(raj_image)[0]



sanjay_image = face_recognition.load_image_file("sanjay.jpeg")
sanjay_encoding = face_recognition.face_encodings(sanjay_image)[0]

sudhanshu_image = face_recognition.load_image_file("sudhanshu1.jpeg")
sudhanshu_encoding = face_recognition.face_encodings(sudhanshu_image)[0]

sahil_image = face_recognition.load_image_file("sahil1.jpeg")
sahil_encoding = face_recognition.face_encodings(sahil_image)[0]

known_face_encodings = [garv_encoding,aashi_encoding, raj_encoding, sanjay_encoding,sudhanshu_encoding,sahil_encoding]
known_face_names = ["Garv","Aashi", "Raj","Sanjay", "Sudhanshu","Sahil"]
# Copy list for attendance
students = known_face_names.copy()


# Create CSV file
current_date = datetime.now().strftime("%Y-%m-%d")
f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    ret, frame = video_capture.read()

    if not ret or frame is None:
        print("Frame not received. Reconnecting...")
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        name = "Unknown"
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # face emotions detector 
        try: 
            result = DeepFace.analyze(frame, actions=['emotion'],enforce_detection=False)
            dominant_emotion = result[0]['dominant_emotion']

        except:
            dominant_emotion = "neutral"

        if dominant_emotion not in ["happy", "sad", "neutral"]:
            dominant_emotion = "neutral"



        # Display name and emotion on frame
        cv2.putText(frame, f"{name} ({dominant_emotion})",(10, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

        # Mark attendance only once
        if name != "Unknown" and name in students:
            students.remove(name)
            current_time = datetime.now().strftime("%H:%M:%S")  # moved inside loop
            lnwriter.writerow([name, current_time])
            print(name, "Marked Present at", current_time)

            hour = datetime.now().hour
            if 5<= hour < 12 :
                greeting = "Good Morning"
            elif 12<=hour<16:
                greeting = "Good Afternoon"
            elif 16<= hour < 21:
                greeting = "Good Evening"
            else :
                greeting = "Hello"

            # random welcoming txt
            welcome_lines = [
                f"{greeting} {name} , have a nice day",
                f"{greeting} {name} , great to see you",
                f"{greeting} {name} , welcome to the class",
                f"{greeting} {name} , hope you are doing well",
                f"{greeting} {name} , your attendece is marked"
            ]

            line = random.choice(welcome_lines)

            engine = pyttsx3.init()
            if dominant_emotion == "happy":
                engine.say(f"{line}. You look happy today")
            elif dominant_emotion == "sad":
                engine.say(f"{line}.You look sad buddy")
                           
            elif dominant_emotion == "neutral":
                engine.say(f"{line}.You look tired buddy")
                            
            
            engine.runAndWait()


            # full_line = f"{line}. You look {dominant_emotion} today."
            # engine.say(full_line)
            # engine.setProperty('rate', 110)

             
            
                 
        elif name == "Unknown":
             engine=pyttsx3.init()
             
             engine.say("Unknown person detected!!!")
             engine.runAndWait()

                
    cv2.imshow("Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
