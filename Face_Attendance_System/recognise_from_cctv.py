import cv2
import face_recognition
import pickle
from datetime import datetime

# === [1] Load known encodings ===
with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

# === [2] Connect to CCTV Camera ===
CAMERA_URL = "http://192.168.1.116:8080/video"  # Replace with your stream URL
cap = cv2.VideoCapture(CAMERA_URL)

if not cap.isOpened():
    print("[❌] Unable to connect to CCTV camera!")
    exit()

print("[✅] CCTV stream started. Press 'q' to quit.")

# === [3] Start Live Recognition ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("[❌] Frame not received from camera.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect and encode faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through each detected face
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Unknown"
        reg_no = "N/A"

        if True in matches:
            matched_idx = matches.index(True)
            name = data["names"][matched_idx]
            reg_no = data["ids"][matched_idx]

        # Draw box and label
        top, right, bottom, left = [v * 4 for v in face_location]  # Scale back up
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        label = f"{name} ({reg_no})"
        cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        print(f"[🧠] Recognised: {name} ({reg_no}) at {datetime.now().strftime('%H:%M:%S')}")

    # Show the frame
    cv2.imshow("CCTV Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
