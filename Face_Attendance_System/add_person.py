import cv2
import os
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox


# Function to add a new person
def add_new_person():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    name = simpledialog.askstring("Input", "Enter Full Name:")
    reg_no = simpledialog.askstring("Input", "Enter Register Number:")

    if not name or not reg_no:
        messagebox.showerror("Error", "Both name and register number are required.")
        return

    # Create folder with format RegNo_Name
    safe_name = name.replace(" ", "_")
    person_folder = f"dataset/{reg_no}_{safe_name}"
    os.makedirs(person_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < 10:
        ret, frame = cap.read()
        if not ret:
            break

        # Add watermark
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        watermarked_frame = frame.copy()
        cv2.putText(watermarked_frame, timestamp, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Save image
        file_path = os.path.join(person_folder, f"{timestamp}.jpg")
        cv2.imwrite(file_path, watermarked_frame)
        count += 1

        cv2.imshow("Capturing Images", watermarked_frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ {name} ({reg_no}) added successfully!")


# Run the function when the script is executed
if __name__ == "__main__":
    add_new_person()
