from file_processing.file_manager import *
from user_management.user_handler import *
from Utils.string_tools import *


def string_ops(choice):
    while True:
        match choice:
            case 1:
                user1=input("Enter the String : ")
                try:
                    print(f"The length of string is {word_Count(user1)}")
                except Exception as e:
                    print(e)
            case 2:
                try:
                    user1=input("Enter the String : ")
                    print(f"The reverse of the string is {reverse_words(user1)}")
                except Exception as e:
                    print(e)
            case 3:
                try:
                    user1=input("Enter the String : ")
                    print(f"The string is palindrome : {check_palindrome(user1)}")
                except Exception as e:
                    print(e)
            case 4:
                try:
                    user1=input("Enter the String : ")
                    print(f"The most common word is {find_Most_Commom(user1)}")
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
    users={}
    while True:
        try:
            print("****************************** Main Menu ******************************")
            print("1. Text Analysis")
            print("2. User Management")
            print("3. File Processing")
            print("4. Exit")

            choice = int(input("Enter your choice: "))
            match choice:
                case 1:
                    print("******************************Welcome to the text analysis ******************************")
                    print(" Enter 1 to get word count \n Enter 2 to reverse input \n Enter 3 to palindrome \n Enter 4 to find most common words \n Enter 5 to exit")
                    try:
                        input_one=int(input("Enter the String choice : "))
                        string_ops(input_one)
                    except ValueError:
                        print("Invalid choice\n")
                case 2:
                    print("******************************Welcome to the user management system******************************")
                    print(" Enter 1 to add user \n Enter 2 to update user \n Enter 3 to get user info \n Enter 4 to remove user \n Enter 5 to exit")
                    try:
                        input1=int(input("Enter your choice : "))
                        user_management(users,input1)
                        if input1==5:
                            break
                    except ValueError:
                        print("Invalid choice\n")
                    except Exception as e:
                        print(e)
                case 3:
                    pass
                case 4:
                    break
        except ValueError:
            print("Invalid choice\n")



if __name__ == "__main__":
    main_menu() 