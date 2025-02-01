from file_processing.file_manager import *
from user_management.user_handler import *
from Utils.string_tools import *
summery=[]
def string_ops(choice):
    while True:
        match choice:
            case 1:
                user1=input("Enter the String : ")
                try:
                    result=word_Count(user1)
                    summery.append(f"The length of string is {result}")
                    print(f"The length of string is {result}")
                except Exception as e:
                    print(e)
            case 2:
                try:
                    user1=input("Enter the String : ")
                    result=reverse_words(user1)
                    summery.append(f"The reverse of the string is {result}")
                    print(f"The reverse of the string is {result}")
                except Exception as e:
                    print(e)
            case 3:
                try:
                    user1=input("Enter the String : ")
                    result=check_palindrome(user1)
                    summery.append(f"The string is palindrome : {result}")
                    print(f"The string is palindrome : {result}")
                    # print(f"The string is palindrome : {result}")
                except Exception as e:
                    print(e)
            case 4:
                try:
                    user1=input("Enter the String : ")
                    result=find_Most_Commom(user1)
                    summery.append(f"The most common word is {result}")
                    print(f"The most common word is {result}")
                except Exception as e:
                    print(e)
            case _:
                break
        choice=int(input("Enter your choice : "))
    return None


def user_management(users,choice):
    
    while True:
        match choice:
            case 1:
                user1=input("Enter the username : ")
                age=int(input("Enter the age : "))
                try:
                    print(add_user(users,user1,age))
                except Exception as e:
                    print(e)
            case 2:
                print(" Enter 1 if you want to update username \n Enter 2 if you want to update age")
                choice1=int(input(" Enter your choice : "))
                user_name = input("Enter the username to update: ")
                match choice1:
                    case 1:
                        try:
                            new_username=input("    Enter the new username: ")
                            print(update_username(users,user_name, new_username))
                        except Exception as e:
                            print(e)
                    case 2:
                        try:
                            new_age=int(input("     Enter the new age to update: "))
                            print(update_user_age(users,user_name, new_age))
                        except Exception as e:
                            print(e)
            case 3:
                username=input("Enter the username to get info: ")
                try:
                    print(get_user_info(users,username))
                except Exception as e:
                    print(e)
            case 4:
                remove1=input("Enter the username to remove: ")
                try:
                    print(remove_user(users,remove1))
                except Exception as e:
                    print(e)
            case _:
                break
        choice=int(input("Enter your choice : "))
    return users



def main_menu():
    users=[]
    while True:
        try:
            print("\n")
            print("****************************** Main Menu *********************************************")
            print("1. Text Analysis")
            print("2. User Management")
            print("3. File Processing")
            print("4. Exit")
            print("**************************************************************************************")
            print("\n")
            choice = int(input("Enter your choice: "))
            match choice:
                case 1:
                    print("\n")
                    print("******************************Welcome to the text analysis ******************************")
                    print(" Enter 1 to get word count \n Enter 2 to reverse input \n Enter 3 to palindrome \n Enter 4 to find most common words \n Enter 5 to exit")
                    print("*****************************************************************************************")
                    print("\n")
                    try:
                        input_one=int(input("Enter the String choice : "))
                        string_ops(input_one)
                    except ValueError:
                        print("Invalid choice\n")
                case 2:
                    print("\n")
                    print("******************************Welcome to the user management system******************************")
                    print(" Enter 1 to add user \n Enter 2 to update user \n Enter 3 to get user info \n Enter 4 to remove user \n Enter 5 to exit")
                    print("**************************************************************************************")
                    print("\n")
                    try:
                        input1=int(input("Enter your choice : "))
                        user_management(users,input1)
                    except ValueError:
                        print("Invalid choice\n")
                    except Exception as e:
                        print(e)
                case 3:
                    print("\n")
                    print("******************************Welcome to the file processing system******************************")
                    print(" Enter 1 to load users from file \n Enter 2 to save users to file \n Enter 3 to write summary \n Enter 4 to exit")
                    print("*************************************************************************************************")
                    print("\n")                   
                    try:
                        while True:
                            input2=int(input("Enter your choice : "))
                            match input2:
                                case 1:
                                    try:
                                        users=load_users_from_file("users_data.txt")
                                        print("Users loaded successfully")
                                    except Exception as e:  
                                        print(e)
                                case 2:
                                    try:
                                        save_users_to_file("users_data.txt",users)
                                        print("Users saved successfully")
                                    except Exception as e:
                                        print(e)

                                case 3:
                                    try:
                                        summery_text="\n".join(map(str,summery))
                                        write_summery("summary_of_data.txt",summery_text)
                                        print("Summary written successfully")
                                    except Exception as e: 
                                        print(e)
                                case 4:
                                    break
                    except ValueError:
                        print("Invalid choice\n")
                    except Exception as e:
                        print(e)
                    pass
                case 4:
                    break
        except ValueError:
            print("Invalid choice\n") 



if __name__ == "__main__":
    main_menu() 