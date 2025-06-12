import os
import cv2
import numpy as np
import face_recognition
import datetime
import pandas as pd
import pickle
import tkinter as tk
from tkinter import simpledialog, messagebox

ENCODINGS_FILE = "encodings.pickle"

# Load Existing Face Data
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    known_face_encodings = data.get("encodings", [])
    known_face_names = data.get("names", [])
    known_face_ids = data.get("ids", [])
else:
    known_face_encodings, known_face_names, known_face_ids = [], [], []

# Periods Definition
PERIODS = {
    "Period 1": (10, 0),
    "Period 2": (10, 50),
    "Period 3": (11, 40),
    "Period 4": (12, 30),
    "Period 5": (14, 10),  # After Lunch
    "Period 6": (15, 0),
    "Period 7": (16, 0),
}

# Get Current Period
def get_current_period():
    now = datetime.datetime.now().time()
    for period, (start_hour, start_minute) in PERIODS.items():
        period_start = datetime.time(start_hour, start_minute)
        period_end = (datetime.datetime.combine(datetime.date.today(), period_start) + datetime.timedelta(
            minutes=50)).time()
        if period_start <= now <= period_end:
            return period
    return None

# Mark Attendance in the Same Row
def mark_attendance(name, reg_no):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    attendance_file = f"attendance_{date_str}.xlsx"
    current_period = get_current_period()

    if not current_period:
        print(f"⏳ No active period. Attendance skipped for {name} ({reg_no}).")
        return

    # Read or Create DataFrame
    if os.path.exists(attendance_file):
        df = pd.read_excel(attendance_file, engine="openpyxl")
    else:
        df = pd.DataFrame(columns=["Reg No", "Name"] + list(PERIODS.keys()))

    # Ensure 'Reg No' column is treated as a string
    df["Reg No"] = df["Reg No"].astype(str)

    # Check if the student already exists in the file
    mask = df["Reg No"] == str(reg_no)

    if mask.any():
        idx = df.loc[mask].index[0]

        # Auto-mark missed periods as ❌
        for period, (hour, minute) in PERIODS.items():
            period_end = datetime.datetime.combine(datetime.date.today(),
                                                   datetime.time(hour, minute)) + datetime.timedelta(minutes=50)
            if now > period_end and pd.isna(df.at[idx, period]):
                df.at[idx, period] = "❌"

        # Mark attendance for the current period
        if pd.isna(df.at[idx, current_period]) or df.at[idx, current_period] == "❌":
            df.at[idx, current_period] = "✅"
            print(f"✅ Attendance updated for {name} ({reg_no}) in {current_period}.")
        else:
            print(f"⏳ {name} ({reg_no}) already marked for {current_period}. Skipping...")

    else:
        # New Entry for Student
        new_entry = {col: "❌" for col in df.columns}
        new_entry["Reg No"], new_entry["Name"] = reg_no, name
        new_entry[current_period] = "✅"

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        print(f"✅ New student entry recorded for {name} ({reg_no}) in {current_period}.")

    # Save the updated attendance
    try:
        with pd.ExcelWriter(attendance_file, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, index=False)
        print(f"📁 Attendance successfully saved in {attendance_file}.")
    except Exception as e:
        print(f"⚠ Error saving attendance: {e}")

# Function to ask for new person details
def ask_new_person_details():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    name = simpledialog.askstring("New Person", "Enter Full Name:")
    reg_no = simpledialog.askstring("New Person", "Enter Register Number:")

    if not name or not reg_no:
        messagebox.showerror("Error", "Name and Register Number are required!")
        return None, None

    return name, reg_no

# Function to save new person details
def save_new_person(face_encoding, name, reg_no):
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)
    known_face_ids.append(reg_no)

    data = {"encodings": known_face_encodings, "names": known_face_names, "ids": known_face_ids}

    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    print(f"✅ New person added: {name} ({reg_no})")

# Recognize Faces and Mark Attendance
def recognize_person():
    cap = cv2.VideoCapture(0)
    recognized_today = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                reg_no = known_face_ids[first_match_index]

                if (name, reg_no) not in recognized_today:
                    mark_attendance(name, reg_no)
                    recognized_today.add((name, reg_no))

                    # === 📸 Save Watermarked Image to Daily Folder ===
                    now = datetime.datetime.now()
                    today_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H-%M-%S")
                    daily_folder = os.path.join("dataset", today_str)
                    os.makedirs(daily_folder, exist_ok=True)

                    safe_name = name.replace(" ", "_")
                    file_name = f"{reg_no}_{safe_name}_{time_str}.jpg"
                    save_path = os.path.join(daily_folder, file_name)
                    watermark_text = f"{name} | {reg_no} | {now.strftime('%Y-%m-%d %H:%M:%S')}"

                    snapshot = frame.copy()
                    cv2.putText(snapshot, watermark_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imwrite(save_path, snapshot)
                    print(f"📸 Saved snapshot: {save_path}")

                else:
                    print(f"⏳ {name} ({reg_no}) already marked today. Skipping...")

            else:
                # Ask for new person's details and save the new person
                name, reg_no = ask_new_person_details()
                if name and reg_no:
                    save_new_person(face_encoding, name, reg_no)
                    recognized_today.add((name, reg_no))
                    mark_attendance(name, reg_no)

                    # === 📸 Save Watermarked Image for New Person ===
                    now = datetime.datetime.now()
                    today_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H-%M-%S")
                    daily_folder = os.path.join("dataset", today_str)
                    os.makedirs(daily_folder, exist_ok=True)

                    safe_name = name.replace(" ", "_")
                    file_name = f"{reg_no}_{safe_name}_{time_str}.jpg"
                    save_path = os.path.join(daily_folder, file_name)
                    watermark_text = f"{name} | {reg_no} | {now.strftime('%Y-%m-%d %H:%M:%S')}"

                    snapshot = frame.copy()
                    cv2.putText(snapshot, watermark_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imwrite(save_path, snapshot)
                    print(f"📸 Saved snapshot: {save_path}")

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_person()