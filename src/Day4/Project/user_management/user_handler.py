
def add_user(users,username,age):
    try:
        if username in users:
            raise ValueError(f"User with username {username} already exists")
        elif age<=0:
            raise ValueError("Age cannot be negative")
        else:
            users[username]=age
            return (f"User with username : {username} is added successfully")
    except TypeError:
        return "Error in input data type"

def remove_user(users,username):
    try :
        if username in users:
            users.pop(username)
            return (f"User with username : {username} is removed successfully")
        else:
            raise ValueError(f"User with username : {username} does not exist")
    except TypeError:
        return "Error in input data type"
    
def get_user_info(users,username):
    try:
        if username in users:
            return (f"User with username : {username} is {users[username]} years old")
        else:
            return (f"User with username : {username} does not exist")
    except ValueError:
        return "Error in input"

def update_user_age(users,username,new_age):
    try:
        if username in users:
            users[username]=new_age
            return (f"User with username : {username} is updated successfully")
        else:
            raise (f"User with username : {username} does not exist")
    except TypeError:
        return "Error in input datatype" 
    

def update_username(users,username,new_name):
    try:
        if username in users:
            users[new_name]=users.pop(username)
            return (f"User with username : {username} is updated successfully")
        else:
            raise (f"User with username : {username} does not exist")
    except TypeError:
        return "Error in input datatype" 
