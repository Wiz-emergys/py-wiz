'''
3. Write python code that allows users to register new accounts, log in to existing
accounts, and reset their passwords.
1. For new registration, store unique username and password in text file
2. For log in check login is valid or not
3. For password change, check for username and change the password
4. Use proper error handling
5. Data should be stored: username1,password_hash1,email_or_phone1
6. Store data in separate folder for employee login, admin login, manager
login, etc.
7. Use os module to create proper directory structure. Check if directories
and files if they are exists.
8. Create a user interface using Streamlit

'''

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


