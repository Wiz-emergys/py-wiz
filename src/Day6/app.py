
# #q1
# import json

# # Load JSON data into a Python data structure
# wi 
# # Results
# print("States with multiple area codes:")
# print(states_with_multiple_area_codes)
# print("\nTotal number of area codes per state:")
# print(area_code_count)
# print(f"\nState with the highest number of area codes: {max_area_code_state} ({max_area_code_count} area codes)")



#2
# import json

# # Example Python dictionary
# example_dict = {
#     "name": "California",
#     "population": 39538223,
#     "area_codes": ["209", "213", "310", "323"],
#     "capital": "Sacramento",
#     "founded": 1850
# }

# # Convert dictionary to JSON, sorting by keys and adding indent
# sorted_json_data = json.dumps(example_dict, indent=4, sort_keys=True)

# # Print the JSON data
# print("JSON Data (Sorted by Keys):")
# print(sorted_json_data)

#   3

import os
import hashlib
import streamlit as st


# Directory structure
BASE_DIR = "user_data"
USER_TYPES = ["employee", "admin", "manager"]

# Ensure directories exist
for user_type in USER_TYPES:
    os.makedirs(os.path.join(BASE_DIR, user_type), exist_ok=True)

# Helper function: Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function: Write user data to file
def write_user_data(file_path, username, password_hash, email_or_phone):
    with open(file_path, "w") as f:
        f.write(f"{username},{password_hash},{email_or_phone}")

# Registration function
def register_user(user_type, username, password, email_or_phone):
    file_path = os.path.join(BASE_DIR, user_type, f"{username}.txt")
    if os.path.exists(file_path):
        st.error("Username already exists. Please choose a different username.")
        return
    password_hash = hash_password(password)
    write_user_data(file_path, username, password_hash, email_or_phone)
    st.success(f"User '{username}' registered successfully!")

# Login function
def login_user(user_type, username, password):
    file_path = os.path.join(BASE_DIR, user_type, f"{username}.txt")
    if not os.path.exists(file_path):
        st.error("Username does not exist.")
        return False
    with open(file_path, "r") as f:
        stored_username, stored_password_hash, _ = f.read().split(",")
    if stored_password_hash == hash_password(password):
        st.success("Login successful!")
        return True
    else:
        st.error("Invalid password.")
        return False

# Reset Password function
def reset_password(user_type, username, new_password):
    file_path = os.path.join(BASE_DIR, user_type, f"{username}.txt")
    if not os.path.exists(file_path):
        st.error("Username does not exist.")
        return
    with open(file_path, "r") as f:
        stored_username, _, stored_email_or_phone = f.read().split(",")
    new_password_hash = hash_password(new_password)
    write_user_data(file_path, stored_username, new_password_hash, stored_email_or_phone)
    st.success("Password updated successfully!")

# Streamlit User Interface
st.title("User Management System")

# Sidebar menu
menu = st.sidebar.selectbox("Choose an option", ["Register", "Login", "Reset Password"])
user_type = st.selectbox("Select User Type", USER_TYPES)

if menu == "Register":
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email_or_phone = st.text_input("Email or Phone")
    if st.button("Register"):
        if username and password and email_or_phone:
            register_user(user_type, username, password, email_or_phone)
        else:
            st.error("All fields are required.")

elif menu == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            login_user(user_type, username, password)
        else:
            st.error("All fields are required.")

elif menu == "Reset Password":
    st.header("Reset Password")
    username = st.text_input("Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Reset Password"):
        if username and new_password:
            reset_password(user_type, username, new_password)
        else:
            st.error("All fields are required.")


