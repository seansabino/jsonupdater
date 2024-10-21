import streamlit as st
import pandas as pd
import json

def set_nested_value(data, keys, value):
    """Set a value in a nested object in data based on a list of keys."""
    for key in keys[:-1]:
        data = data[key]
    data[keys[-1]] = value

# Streamlit app
st.title("JSON Updater App")

# Upload JSON file
json_file = st.file_uploader("Upload JSON File", type="json")
csv_file = st.file_uploader("Upload CSV File (Location in JSON, Updated Text)", type="csv")

if json_file and csv_file:
    # Read JSON
    data = json.load(json_file)

    # Read CSV
    df = pd.read_csv(csv_file)

    # Process the CSV and update JSON
    for index, row in df.iterrows():
        location = row['Location in JSON']
        updated_text = row['Updated Text']  # Replacing "URL" with "Updated Text"
        keys = location.split('.')
        try:
            set_nested_value(data, keys, updated_text)
        except KeyError:
            st.error(f"KeyError: '{location}' not found in JSON")

    # Create a download button for the updated JSON file
    updated_json = json.dumps(data, indent=4)
    st.success("JSON has been updated! You can download the updated file below.")
    st.download_button(label="Download Updated JSON",
                       data=updated_json,
                       file_name="updated_data.json",
                       mime="application/json")
