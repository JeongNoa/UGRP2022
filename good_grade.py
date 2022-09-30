import pandas as pd
import numpy as np

#n = int(input("목표학점"))

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
for i in sub_num:
    subject_grade[i] = np.array([float(0)]*19)

for i in subject.iloc():
    if i["학수번호"].split('-')[0] in subject_grade:
        continue
    else:
        subject_grade[i["학수번호"].split('-')[0]] = i["교과목"]

for i in subject.iloc():
    subject_grade[i["학수번호"].split('-')[0]] += np.array([i["A+"],i["A0"],i["A-"],i["B+"],i["B0"],i["B-"],i["C+"],i["C0"],i["C-"],i["D+"],i["D0"],i["D-"],i["F"],i["S"],i["U"],i["SA"],i["W"],i["I"],i["GPA계산인원"]])  

sub_data = []
for i in subject_grade:
    print(i, subject_grade[i])