import pandas as pd
import os

EXCEL_FILE = "attendance.xlsx"

# Define period names
periods = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6", "Period 7"]

# Check if the Excel file exists
if os.path.exists(EXCEL_FILE):
    try:
        # Load existing data with openpyxl engine
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")

        # Ensure all period columns exist
        for period in periods:
            if period not in df.columns:
                df[period] = ""  # Add missing period columns

        # Save the updated file
        df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
        print("✅ Excel sheet updated successfully!")

    except Exception as e:
        print(f"❌ Error reading the Excel file: {e}")
        print("🛠️ Try deleting 'attendance.xlsx' and re-running this script.")

else:
    # Create a new DataFrame with the required columns
    df = pd.DataFrame(columns=["Name", "Date"] + periods)
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
    print("✅ New Excel sheet created with period-wise columns!")
