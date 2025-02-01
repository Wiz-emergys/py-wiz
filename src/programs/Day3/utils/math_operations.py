

def add(a,b):
    '''Performed '''
    try:
        print(f"The sum of {a} + {b} is :",a+b)
    except:
        print("Wrong Input provided cant perfrom the operations")

def substract(a,b):
    try:
        print(f"The substraction of {a}- {b} is :",a-b)
    except:
        print("Wrong Input provided cant perfrom the operations")

def multiply(a,b):
    try:
        print(f"The Multiplication of {a}*{b} is :",a*b)
    except:
        print("Wrong Input provided cant perfrom the operations")
    
def divide(a,b):
    try:
        print(f"The Division of {a} / {b} is :",a/b)
    except ZeroDivisionError:
        print(f"Division by Zero is not supported..")
    except TypeError:
        print("Cant perform division inavalid input type")
    finally:
        print("Thanks For visiting")
        