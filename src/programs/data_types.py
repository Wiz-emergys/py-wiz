# # simple program to implement dAta TYypes and loops in python

# integer=10
# floating=10.5
# stringfy="Hello"
# lister=[1,2,3,4,5]
# tuples=(1,2,3,4,5) 
# seter={1,2,3,4,5}
# dicts={1:"one",2:"two",3:"three",4:"four",5:"five"}
# yes=True

# print(f"Integer : {integer}")   
# print(f"Floating : {floating}")
# print(f"String : {stringfy}")
# print(f"List : {lister}")
# print(f"Tuples : {tuples}")
# print(f"Set : {seter}")
# print(f"Dictionary : {dicts}")
# print(f"Boolean : {yes}")

# # Loops
# print("Looping through List")
# for i in lister:
#     print("loop item are:",i)

# print("Looping through Tuples")
# for i in tuples:
#     print("tupel item are:",i)

# print("Looping through Set")    
# for i in seter:
#     print("set item are:",i)

# print("Looping through Dictionary")
# for i,v in dicts.items():
#     print(f"dict key is {i} value is {v}")


# #while loop
# i=0
# while i<5:
#     print(i)
#     if(i==3):
#         print("Breaking the loop")
#         break
#     i+=1


# # for each loop=
# for i in "Hello":
#     print(i)

# # List Comprehension
# lister=[i for i in range(10)]
# print(lister)

# # List Comprehension with condition
# lister=[i for i in range(10) if i%2==0]
# print(lister)


#print the first 10 numbers and in each interation print the sum of current and previous number
sum=0
for i in range(1,11):
    sum+=i
    print(f"Current Number is {i} and sum is {sum}")