import face_recognition
import os
import pickle

DATASET_PATH = "dataset/"
ENCODINGS_FILE = "encodings.pickle"


def encode_faces():
    known_encodings = []
    known_names = []
    known_ids = []  # Stores Registered Numbers

    print("[INFO] Checking dataset folder...")
    if not os.path.exists(DATASET_PATH):
        print("[❌] Dataset folder not found!")
        return

    for folder_name in os.listdir(DATASET_PATH):
        person_path = os.path.join(DATASET_PATH, folder_name)

        # Extract Registered Number & Name from folder name (Format: "RegNo_Name")
        if "_" in folder_name:
            reg_no, person_name = folder_name.split("_", 1)
        else:
            print(f"[⚠️] Skipping '{folder_name}' (Invalid format, should be 'RegNo_Name')")
            continue  # Skip folders without correct format

        print(f"[INFO] Processing {person_name} ({reg_no})...")

        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)
            print(f"  -> Encoding {image_name}...")

            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)
                known_ids.append(reg_no)  # Store Registered Number
                print(f"  ✅ {image_name} encoded successfully!")
            else:
                print(f"  ❌ No face found in {image_name}!")

    # Save encodings, names, and IDs
    data = {"encodings": known_encodings, "names": known_names, "ids": known_ids}
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    print("[INFO] Face encoding complete!")
    print(f"[INFO] Encodings saved to {ENCODINGS_FILE}")


if __name__ == "__main__":
    encode_faces()
