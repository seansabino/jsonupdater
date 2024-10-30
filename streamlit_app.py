import streamlit as st
import pandas as pd
import json

def set_nested_value(data, keys, value):
    """Set a value in a nested object in data based on a list of keys."""
    for key in keys[:-1]:
        data = data.get(key, {})  # Safely get the nested dictionary
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
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()

    # Process the CSV and update JSON
    for index, row in df.iterrows():
        location = row.get('Location in JSON')
        updated_text = row.get('Updated Text')  # Replacing "URL" with "Updated Text"

        # Check if the location and updated_text are valid
        if pd.isna(location) or pd.isna(updated_text):
            st.warning(f"Skipping row {index} due to missing data in 'Location in JSON' or 'Updated Text'")
            continue

        try:
            keys = location.split('.')
            set_nested_value(data, keys, updated_text)
        except AttributeError as e:
            st.error(f"Error at row {index}: {e}")
        except KeyError as e:
            st.error(f"KeyError: '{location}' not found in JSON structure at row {index}")

    # Create a download button for the updated JSON file
    updated_json = json.dumps(data, indent=4)
    st.success("JSON has been updated! You can download the updated file below.")
    st.download_button(label="Download Updated JSON",
                       data=updated_json,
                       file_name="updated_data.json",
                       mime="application/json")
