#Remove all occurrences of a specific value from list 
# lister = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
# value_to_remove = 2
# for x in lister:
#     if x == value_to_remove:
#         lister.remove(x)
# print("Original List : ", lister)



# #Find intersection of two lists 
# list1 = [1, 2, 3, 3, 4, 5]
# list2 = [3,3, 4, 5, 6, 7]
# intersection = [value for value in list1 if value in list2]
# print("Intersection of two lists : ", intersection)

#Get smallest, largest number from list 
# lister = [1, 2, 3, 4, 5]
# print(f"Smallest number is : { min(lister)} and Largest number is : {max(lister)}")




#Write a Python program to get a list, sorted in increasing order by the last element in each tuple from a given list of non-empty tuples 

# Sample list = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)] 
#Expected output = [(2, 1), (1, 2), (2, 3), (4, 4), (2, 5)] \

# lister = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]
# for i in range(0, len(lister)):
#     for j in range(i+1, len(lister)):
#         if lister[i][-1] > lister[j][-1]:
#             lister[i], lister[j] = lister[j], lister[i]
#             print("Sorted list by last element of tuple : ", lister)

#Write a python program to make star pattern

# n = 5
# for i in range(n):
#     print("   " * (n - i - 1) + " * " * (2 * i + 1))
# for i in range(n - 2, -1, -1):
#     print("   " * (n - i - 1) + " * " * (2 * i + 1))

'''Develop a program to calculate the final grades of students based on their scores in three exams: Exam 1, Exam 2, and Exam 3. The final grade is calculated as follows: 
If the average score is greater than or equal to 90, the grade is 'A'. 
If the average score is greater than or equal to 80 and less than 90, the grade is 'B'. 
If the average score is greater than or equal to 70 and less than 80, the grade is 'C'. 
If the average score is greater than or equal to 60 and less than 70, the grade is 'D'. 
If the average score is less than 60, the grade is 'F'. 
Tasks: '''

# num_students = int(input("Enter the number of students: "))
# students = []
 
# for _ in range(num_students):
#     name = input("Enter the student's name: ")
#     exam1 = float(input("Enter the score for Exam 1: "))
#     exam2 = float(input("Enter the score for Exam 2: "))
#     exam3 = float(input("Enter the score for Exam 3: "))
   
#     average_score = (lambda e1, e2, e3: (e1 + e2 + e3) / 3)(exam1, exam2, exam3)
   
#     if average_score >= 90:
#         grade = 'A'
#     elif average_score >= 80:
#         grade = 'B'
#     elif average_score >= 70:
#         grade = 'C'
#     elif average_score >= 60:
#         grade = 'D'
#     else:
#         grade = 'F'
   
#     students.append({
#         'name': name,
#         'exam1': exam1,
#         'exam2': exam2,
#         'exam3': exam3,
#         'average_score': average_score,
#         'grade': grade
#     })
 
# print("\nStudent Data:")
# print(f"{'Name':<15}{'Exam 1':<10}{'Exam 2':<10}{'Exam 3':<10}{'Average':<10}{'Grade':<5}")
# for student in students:
#     print(f"{student['name']:<15}{student['exam1']:<10}{student['exam2']:<10}{student['exam3']:<10}{student['average_score']:<10.2f}{student['grade']:<5}")

list1 = [1, 2,3, 4, 5, 3]
list2 = [3, 3, 3,4, 5, 6, 7]


intersection=[]
temp_list=list2.copy()
for value in list1:
    if value in temp_list:
        intersection.append(value)
        temp_list.remove(value)
print(intersection)
