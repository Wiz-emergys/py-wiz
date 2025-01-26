
import json
def save_users_to_file(filename,users):
    try:
        with open(filename,'w') as file:
            # for user in users:
                # /file.write(f"{user},{users[u#ser]},{user[age]}\n")
            json.dump(users,file,indent=4)
        return "Users saved successfully"
    except PermissionError:
        return "Permissioon Denied"
    except FileNotFoundError:
        return "Error file not found error"
    except Exception as e:  
        return e
    
def load_users_from_file(filename):
    try:
        with open(filename,'r') as file:
            users = json.load(file)
        return users
    except FileNotFoundError:
        return "Error file not found error"
    except PermissionError:
        return "Error in permission  access"
    except Exception as e:
        return e
    
def write_summery(file,text_analysis):
    try: 
        with open(file,'w') as file:
            file.write(text_analysis)
        return "Summery written successfully"
    except FileNotFoundError:
        return "File not found" 
    except PermissionError:
        return "Error in input data type"
    except Exception as e:
        return e

