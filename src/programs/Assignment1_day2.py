
''' This is day 2 assignment file for the python course 
which contents practice quetions cobvering the following topics:
1.Loops
2. Functions
3. Lambda functions
4. List 
5.patterns
'''
#Write a Python program that accepts three lists and finds the elements that are unique across all three lists (i.e., appear in only one of the lists). 
# list1=[1,2,3,4,5,6,7,8,9]
# list2=[2,3,5,6,7,8,9,10]
# list3=[3,5,6,7,8,9,10,11]

# list_out=[]
# for i in list1:
#     if i not in list2 and i not in list3:
#         list_out.append(i)

# for i in list2:
#     if i not in list1 and i not in list3:
#         list_out.append(i)

# for i in list3:
#     if i not in list1 and i not in list2:
#         list_out.append(i)
# print(list_out)


#Given a list of tuples, group them by their first element and create a dictionary where the keys are the first elements, and the values are lists of corresponding second elements. 
#Example Input: [(1, 2), (2, 3), (1, 4), (3, 5), (2, 6)] 
#Expected Output: {1: [2, 4], 2: [3, 6], 3: [5]} 

# sample_list = [(1, 2), (2, 3), (1, 4), (3, 5), (2, 6)]
# dist={}
# for i in sample_list:
#     key=i[0]
#     if key in dist: 
#         dist[key].append(i[1])
#     else:
#         dist[key]=[i[1]]
# print(dist)


#   Write a program that accepts three lists of integers, merges them into a single list, removes duplicates, and sorts the final list in descending order. 
# list1=[1,2,3,4,5,6,7,8,9]
# list2=[2,3,5,6,7,8,9,10]
# list3=[3,5,6,7,8,9,10,11]
# list_out=list1+list2+list3
# list_out=list(set(list_out))
# list_out.sort(reverse=True)
# print(list_out)


#Write a Python program to filter tuples from a given list where the sum of the elements in the tuple is greater than a specified threshold. 
# Expected Output: [(3, 4), (2, 6)] 
# Input1= [(1, 2), (3, 4), (5, 1), (2, 6)]
# Threshold = 6 
# list=[]

# for i in Input1:
#     if sum(i)>Threshold:
#         list.append(i)
# print(list)


#Develop a program that takes a list of integers and calculates the following statistics using lambda functions: 
# Mean 
# Median 
# Standard deviation 

# import math
# list1=[1,2,3,4,5,6,7,8,9]
# mean = lambda x: sum(x)/len(x)
# median = lambda x: x[len(x)//2] if len(x)%2!=0 else (x[len(x)//2]+x[len(x)//2-1])/2
# std_dev = lambda x: math.sqrt(sum([(i-mean(x))**2 for i in x])/len(x))
# print(mean(list1))
# print(median(list1))
# print(std_dev(list1))


#Write a Python program to find the longest word(s) in a given list of strings. If there are multiple words with the same maximum length, return them all. 
#Expected Output: ['blueberry']
# Input= ['apple', 'banana', 'pear', 'blueberry','blueberrt'] 

# max_len=max([len(i) for i in Input])
# print([i for i in Input if len(i)==max_len])
 

#Write a Python program to count the frequency of each element across all nested lists. 
#Expected Output: {1: 1, 2: 2, 3: 3, 4: 2, 5: 1} 
# Input= [[1, 2, 3], [2, 3, 4], [3, 4, 5]] 

# dict={}
# for sublist in Input :
#     for element in sublist:
#         if element in dict:
#             dict[element]+=1
#         else:
#             dict[element]=1
# print(dict)


#Write a program to sort a dictionary by its values in descending order and return the sorted dictionary. 

Input= { 'a': 3, 'b': 5, 'c': 1, 'd': 4 } 
# sorted_dict= dict(sorted(Input.items(), key=lambda x: x[1], reverse=True))
# print(sorted_dict)

sorted_dict={}
while Input: 
    max_key=None
    for key in Input:
        if max_key is None or Input[key]>Input[max_key]:
            max_key=key
    sorted_dict[max_key]=Input.pop(max_key)
print(sorted_dict)
# Expected Output: { 'b': 5, 'd': 4, 'a': 3, 'c': 1 } 


#Develop a Python program to generate the first N rows of Pascal’s Triangle and store the rows as a list of lists. 

#Example Input: N = 5 

'''Expected Output: 

[ 
  [1], 
  [1, 1], 
  [1, 2, 1], 
  [1, 3, 3, 1], 
  [1, 4, 6, 4, 1] 
] 
'''

# n= 6 
# list1=[[1]]
# for i in range(1,n):
#     list2=[1]
#     for j in range(1,i):
#         list2.append(list1[i-1][j-1]+list1[i-1][j])
#     list2.append(1)
#     list1.append(list2)

# for i in list1:
#     print(i)


#Write a Python program that accepts a list of strings and transforms it into a list of tuples where: 

#The first element of the tuple is the string in uppercase. 
#The second element is the length of the string. 
#The third element is the reversed string. 

# inputs= ['python', 'data', 'science'] 
# list1=[]
# for i in inputs:
#     list1.append((i.upper(),len(i),i[::-1]))
# print(list1)