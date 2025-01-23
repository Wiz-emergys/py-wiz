from utils.math_operations import *

from Data_processing.data_cleaning import remove_duplicates


def perform_math_operations(a,b,value):
    if value in ('add','mul','sub','div'):
        match value:
            case 'add':
                add(a,b)
            case 'sub':
                substract(a,b)
            case 'mul':
                multiply(a,b)
            case 'div':
                divide(a,b)
    else:
        print("Invalid choice")

para1=int(input("Enter first value :"))
para2=int(input("Enter 2nd value : "))
print("select operation \n 1.Add\n 2.Sub \n 3.Mul \n 4.Div")
value=input("enter operations you want to perfrom : ")

 
perform_math_operations(para1,para2,value.lower())


lister=[11,11,2,3,5,5,7,8,9,4,6,533,554,4,4,]

remove_duplicates(lister)