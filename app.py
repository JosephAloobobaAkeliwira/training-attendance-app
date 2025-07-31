import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Training Attendance", page_icon="📝")

# Load today's active shift
try:
    shift_df = pd.read_csv("active_shift.csv")
except FileNotFoundError:
    st.error("❌ 'active_shift.csv' not found. Please upload or place the file in the app folder.")
    st.stop()

# Display Training Info
training_title = "Zipline Daily Training"
training_date = datetime.today().strftime("%Y-%m-%d")

st.title("📋 Training Attendance")
st.subheader(training_title)
st.write(f"📅 Date: **{training_date}**")

# List of names on duty today
name = st.selectbox("Select your name", shift_df["name"].tolist())

# Confirm and submit
confirm = st.checkbox("✅ I confirm that I attended this training")

if confirm and st.button("Submit Attendance"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = pd.DataFrame([{
        "name": name,
        "training": training_title,
        "date": training_date,
        "timestamp": timestamp
    }])

    try:
        log = pd.read_csv("attendance_log.csv")
        log = pd.concat([log, new_entry], ignore_index=True)
    except FileNotFoundError:
        log = new_entry

    log.to_csv("attendance_log.csv", index=False)
    st.success("✅ Attendance recorded!")
