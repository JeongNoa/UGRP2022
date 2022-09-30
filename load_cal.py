import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.linear_model import LinearRegression
import re
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


subject = pd.read_excel('로드계산.xlsx')
subject_load = pd.read_excel('subjects.xlsx')
total_subject = pd.read_csv('total_subjects.csv')
df = []
factors = {}
subs  = {}

ideal_load = {}
for i in range(len(total_subject["과목명"])):
    ideal_load[total_subject["과목명"][i]] = total_subject["신청학점"][i]   

corr_column_names = ['정원', '수강인원','응답인원','강의비율','참여비율','영어강의척도비율',
                     '평점','수업조직',	'수업진행',	'동기부여',	'시험',	'학습결과',	'학생만족',	'실험',	'영어강의',	'office hour']


for i in corr_column_names:
    factors[i] = abs(np.corrcoef(subject['로드'], subject[i])[0, 1])

factors = sorted(factors.items(), key = lambda item: item[1], reverse = True)

for i in factors:
    print(i)

x = subject[['office hour', '시험', '학생만족', '영어강의척도비율', '평점', '실험', '참여비율', '강의비율', '수업진행', '수업조직']]
y = subject[['로드']]
sc = StandardScaler()
sc.fit(x)
 
x_std = sc.transform(x)

lin = LinearRegression()
lin.fit(x_std, y)
svm_model = SVC(kernel='rbf', C=8, gamma=0.7)
 
svm_model.fit(x_std, y)


x_load = subject_load[['office hour', '시험', '학생만족', '영어강의척도비율', '평점', '실험', '참여비율', '강의비율', '수업진행', '수업조직']]

sc = StandardScaler()
sc.fit(x_load)
 
x_load_std = sc.transform(x_load)
svm_y = svm_model.predict(x_load_std).flatten()
lin_y = lin.predict(x_load_std).flatten()
y_load = (np.array(svm_model.predict(x_load_std))+np.array(lin_y))/2

real_load = []

for i in range(len(subject_load["교과목명"])):
    try:
        real_load.append(ideal_load[subject_load["교과목명"][i]]*(y_load[i]+0.5))
    except:
        real_load.append(0)
        
id_ = input("학수번호 ")
for i in range(len(subject_load)):
    string = subject_load["학수번호"][i]
    if id_ in string and int(re.sub(r'[^0-9]', '', string)) < 400: 
        sub = str(subject_load["교과목명"][i])+"_"+str(subject_load["교수명"][i])
        if sub in subs:
            subs[sub] = (subs[sub] + real_load[i])/2
        else:
            subs[sub] = real_load[i]



subs = sorted(subs.items(), key = lambda item: item[1], reverse = True)

for i in subs[:20]:
    print(i)




    
