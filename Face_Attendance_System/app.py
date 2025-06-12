from flask import Flask, jsonify, request
import os
import pickle

app = Flask(__name__)

# Path to the encodings file (you will need this for face recognition)
ENCODINGS_FILE = "encodings.pickle"


# Function to load encodings
def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
        return data.get("encodings", []), data.get("names", []), data.get("ids", [])
    return [], [], []


# Route to mark attendance
@app.route('/attendance', methods=['POST'])
def mark_attendance():
    student_data = request.json  # Get the data from the React front-end
    print(f"Marking attendance for {student_data['name']}")

    # Implement your face recognition logic here

    # If everything works
    return jsonify({"status": "success", "message": "Attendance marked successfully!"})


# Route to add a new person
@app.route('/add_person', methods=['POST'])
def add_person():
    person_data = request.json  # Get new person data from React front-end
    print(f"Adding new person: {person_data['name']}")

    # Save this person's data in your system (e.g., pickle or database)

    return jsonify({"status": "success", "message": "Person added successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
