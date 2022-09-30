import pandas as pd
import numpy as np

goal_grade = float(input("목표학점: "))
my_sub_num = input("학수번호: ")

subject = pd.read_excel('grade(2022).xlsx')
sub_num = []

raw_sub_num = np.array(subject["학수번호"])

for i in raw_sub_num:
    sub = i.split('-')[0]
    if sub in sub_num:
        continue
    else:
        sub_num.append(sub)

subject_grade = {}
sub_name = {}
subject_grade_4_3 = {}
subject_grade_4_0 = {}
subject_grade_3_7 = {}
subject_grade_3_3 = {}
subject_grade_3_0 = {}

for i in sub_num:
    subject_grade[i] = np.array([float(0)]*19)

for i in subject.iloc():
    if i["학수번호"].split('-')[0] in sub_name:
        continue
    else:
        sub_name[i["학수번호"].split('-')[0]] = i["교과목"]

for i in subject.iloc():
    subject_grade[i["학수번호"].split('-')[0]] += np.array([i["A+"],i["A0"],i["A-"],i["B+"],i["B0"],i["B-"],i["C+"],i["C0"],i["C-"],i["D+"],i["D0"],i["D-"],i["F"],i["S"],i["U"],i["SA"],i["W"],i["I"],i["GPA계산인원"]])  

for i in sub_num:
    subject_grade_4_3[i] = subject_grade[i][0]/subject_grade[i][-1]
    subject_grade_4_0[i] = (subject_grade[i][0]+subject_grade[i][1])/subject_grade[i][-1]
    subject_grade_3_7[i] = (subject_grade[i][0]+subject_grade[i][1]+subject_grade[i][2])/subject_grade[i][-1]
    subject_grade_3_3[i] = (subject_grade[i][0]+subject_grade[i][1]+subject_grade[i][2]+subject_grade[i][3])/subject_grade[i][-1]
    subject_grade_3_0[i] = (subject_grade[i][0]+subject_grade[i][1]+subject_grade[i][2]+subject_grade[i][3]+subject_grade[i][4])/subject_grade[i][-1]


subject_grade_4_3 = sorted(subject_grade_4_3.items(), key = lambda item: item[1], reverse = True)
subject_grade_4_0 = sorted(subject_grade_4_0.items(), key = lambda item: item[1], reverse = True)
subject_grade_3_7 = sorted(subject_grade_3_7.items(), key = lambda item: item[1], reverse = True)
subject_grade_3_3 = sorted(subject_grade_3_3.items(), key = lambda item: item[1], reverse = True)
subject_grade_3_0 = sorted(subject_grade_3_0.items(), key = lambda item: item[1], reverse = True)

print(subject_grade_4_3[0][0])
if goal_grade > 4:
    for i in subject_grade_4_3:
        if my_sub_num in i[0]:
            print(sub_name[i[0]], i[1]*100,"%로 목표학점을 위한 학점을 준다")
elif goal_grade > 3.7:
    for i in subject_grade_4_0:
        if my_sub_num in i[0]:
            print(sub_name[i[0]], i[1]*100,"%로 목표학점을 위한 학점을 준다")

elif goal_grade > 3.3:
    for i in subject_grade_3_7:
        if my_sub_num in i[0]:
            print(sub_name[i[0]], i[1]*100,"%로 목표학점을 위한 학점을 준다")

elif goal_grade > 3.0:
    for i in subject_grade_3_3:
        if my_sub_num in i[0]:
            print(sub_name[i[0]], i[1]*100,"%로 목표학점을 위한 학점을 준다")
    
else: 
    for i in subject_grade_3_0:
        if my_sub_num in i[0]:
            print(sub_name[i[0]], i[1]*100,"%로 목표학점을 위한 학점을 준다")

