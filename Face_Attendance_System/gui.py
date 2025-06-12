import os
import shutil
import customtkinter as ctk
import subprocess
import datetime
import pickle
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import webbrowser
import tkinter as tk

ENCODINGS_FILE = "encodings.pickle"


# Ensure encodings.pickle exists; create if missing
def ensure_encodings_file():
    if not os.path.exists(ENCODINGS_FILE):
        print("⚠️ No encodings found. Creating a new encodings.pickle file...")
        data = {"encodings": [], "names": [], "ids": []}
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(data, f)
        print("✅ New encodings.pickle file created successfully!")


# Function to take attendance
def take_attendance():
    status_label.configure(text="Starting attendance system...", text_color="orange")
    root.update()
    try:
        subprocess.run(["python", "recognition_helper.py"])
        status_label.configure(text="Attendance completed successfully!", text_color="green")
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")


# Function to add a new person
def add_new_person():
    status_label.configure(text="Opening registration form...", text_color="orange")
    root.update()
    try:
        subprocess.run(["python", "add_person.py"])
        status_label.configure(text="Registration form closed", text_color="green")
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")


# Function to view attendance records
def view_attendance():
    status_label.configure(text="Opening attendance records...", text_color="orange")
    root.update()
    try:
        # This would launch your attendance viewer (you'd need to create this script)
        subprocess.run(["python", "view_attendance.py"])
        status_label.configure(text="Attendance viewer closed", text_color="green")
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")


# Function to toggle between light and dark mode
def toggle_appearance_mode():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        appearance_btn.configure(text="🌙 Dark Mode")
    else:
        ctk.set_appearance_mode("Dark")
        appearance_btn.configure(text="☀️ Light Mode")


# Function to show about dialog
def show_about():
    about_window = ctk.CTkToplevel(root)
    about_window.title("About Face Attendance System")
    about_window.geometry("400x300")
    about_window.resizable(False, False)

    # Make the dialog modal
    about_window.transient(root)
    about_window.grab_set()

    # About content
    about_frame = ctk.CTkFrame(about_window, corner_radius=10)
    about_frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(about_frame, text="Face Attendance System", font=("Arial", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(about_frame, text=f"Version 1.0.0", font=("Arial", 12)).pack()
    ctk.CTkLabel(about_frame, text=f"© {datetime.datetime.now().year} Your Organization", font=("Arial", 10)).pack(
        pady=5)

    description = "An advanced facial recognition system for automated attendance tracking in educational institutions and workplaces."
    ctk.CTkLabel(about_frame, text=description, wraplength=300).pack(pady=10)

    # Close button
    ctk.CTkButton(about_frame, text="Close", command=about_window.destroy).pack(pady=10)


# Ensure encodings file exists before starting GUI
ensure_encodings_file()

# Create GUI window
ctk.set_appearance_mode("Dark")  # Start with dark mode for modern look
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Face Attendance System")
root.geometry("700x600")
root.minsize(700, 600)  # Set minimum window size

# Create a background frame
bg_frame = ctk.CTkFrame(root, corner_radius=0)
bg_frame.pack(fill="both", expand=True)

# Header frame
header_frame = ctk.CTkFrame(bg_frame, corner_radius=10, fg_color=("gray85", "gray20"))
header_frame.pack(padx=20, pady=(20, 10), fill="x")

# Create a title with icon (you'll need a camera icon file)
title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
title_frame.pack(pady=10)

title_label = ctk.CTkLabel(title_frame, text="Face Attendance System", font=("Arial", 24, "bold"))
title_label.pack(side="left", padx=5)

# Current date and time
date_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
date_frame.pack(pady=5)

now = datetime.datetime.now()
date_str = now.strftime("%A, %d %B %Y")
time_str = now.strftime("%I:%M %p")

date_label = ctk.CTkLabel(date_frame, text=date_str, font=("Arial", 12))
date_label.pack()

time_label = ctk.CTkLabel(date_frame, text=time_str, font=("Arial", 12))
time_label.pack()


# Update time label every second
def update_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
    time_label.configure(text=time_str)
    root.after(1000, update_time)  # Schedule next update after 1 second


update_time()  # Start the clock update

# Content frame
content_frame = ctk.CTkFrame(bg_frame, corner_radius=10)
content_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Left panel for buttons
button_panel = ctk.CTkFrame(content_frame, corner_radius=10, width=200)
button_panel.pack(side="left", padx=10, pady=10, fill="y")

# Button style
button_width = 180
button_height = 40
button_corner = 8
button_font = ("Arial", 14)

# Main function buttons
take_attendance_btn = ctk.CTkButton(
    button_panel,
    text="📸 Take Attendance",
    command=take_attendance,
    width=button_width,
    height=button_height,
    corner_radius=button_corner,
    font=button_font,
    hover_color=("darkblue", "blue")
)
take_attendance_btn.pack(pady=10, padx=10)

add_person_btn = ctk.CTkButton(
    button_panel,
    text="👤 Add New Person",
    command=add_new_person,
    width=button_width,
    height=button_height,
    corner_radius=button_corner,
    font=button_font,
    hover_color=("darkgreen", "green")
)
add_person_btn.pack(pady=10, padx=10)

view_attendance_btn = ctk.CTkButton(
    button_panel,
    text="📊 View Records",
    command=view_attendance,
    width=button_width,
    height=button_height,
    corner_radius=button_corner,
    font=button_font,
    hover_color=("darkpurple", "purple")
)
view_attendance_btn.pack(pady=10, padx=10)

# Right panel for info/visualization
info_panel = ctk.CTkFrame(content_frame, corner_radius=10)
info_panel.pack(side="right", padx=10, pady=10, fill="both", expand=True)

# Welcome message
welcome_label = ctk.CTkLabel(
    info_panel,
    text="Welcome to Face Attendance System",
    font=("Arial", 18, "bold")
)
welcome_label.pack(pady=(20, 10))

info_text = """
This system uses facial recognition technology to automate 
attendance tracking. Just click "Take Attendance" to start 
the camera and recognize registered individuals.

Use "Add New Person" to register new faces in the system.
"""

info_label = ctk.CTkLabel(info_panel, text=info_text, wraplength=300)
info_label.pack(pady=10)

# Stats in the info panel
stats_frame = ctk.CTkFrame(info_panel, corner_radius=10, fg_color=("gray90", "gray17"))
stats_frame.pack(padx=20, pady=20, fill="x")

# Read statistics from the encodings file
try:
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    registered_count = len(data["names"]) if "names" in data else 0
except:
    registered_count = 0

stats_label = ctk.CTkLabel(
    stats_frame,
    text=f"Registered Users: {registered_count}",
    font=("Arial", 14)
)
stats_label.pack(pady=10)

# Status bar
status_frame = ctk.CTkFrame(bg_frame, height=30, corner_radius=0, fg_color=("gray80", "gray25"))
status_frame.pack(fill="x", side="bottom")

status_label = ctk.CTkLabel(status_frame, text="System ready", text_color="green")
status_label.pack(side="left", padx=10)

# Bottom toolbar with additional functions
toolbar_frame = ctk.CTkFrame(bg_frame, corner_radius=10)
toolbar_frame.pack(padx=20, pady=10, fill="x", side="bottom")

# Mode toggle button
appearance_btn = ctk.CTkButton(
    toolbar_frame,
    text="☀️ Light Mode",
    command=toggle_appearance_mode,
    width=120,
    corner_radius=button_corner
)
appearance_btn.pack(side="left", padx=10, pady=10)

# About button
about_btn = ctk.CTkButton(
    toolbar_frame,
    text="ℹ️ About",
    command=show_about,
    width=120,
    corner_radius=button_corner
)
about_btn.pack(side="left", padx=10, pady=10)

# Exit button
exit_btn = ctk.CTkButton(
    toolbar_frame,
    text="🚪 Exit",
    command=root.quit,
    fg_color="red",
    hover_color="darkred",
    width=120,
    corner_radius=button_corner
)
exit_btn.pack(side="right", padx=10, pady=10)

# Run GUI
if __name__ == "__main__":
    root.mainloop()