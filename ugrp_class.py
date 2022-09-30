import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.linear_model import LinearRegression
import re
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import sys
import operator
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic


class Recommend:
    def __init__(self, year, major):
        self.y1 = year
        self.result = self.recommend = pd.read_csv('courses.csv',encoding='UTF8')
        self.subject = list(set(self.recommend['과목명']))
        self.subject_num = list(set(self.recommend['학수번호']))
        self.recommend['학과'] = np.where(self.recommend['학과'] == '단일계열', '무은재학부', self.recommend['학과'])
        self.major = list(set(self.recommend['학과']))
        self.recommend.insert(0,"학년",self.recommend['성적년도']-self.recommend['입학년도']+1,True)
        self.major_dic = {'무은재학부':1, '화학공학과':2, '신소재공학과':3, '화학과':4, '생명과학과':5, 'IT융합공학과':6, '산업경영공학과':7, '컴퓨터공학과':8, '수학과':9,'전자전기공학과':10, '물리학과':11, '기계공학과':12}  
        self.m1 = self.major_dic[major]
        self.data = []
        for i in range(len(self.recommend)):
            self.data.append([self.recommend['학년'][i], self.major_dic[self.recommend['학과'][i]]])
        
    def run_recommend(self):
        self.euclidean_distance()
        return self.recommend_subject()
    def euclidean_distance(self):
        self.length = []
        self.my = [self.y1, self.m1]
 
        for i in self.data:
            self.length.append((self.my[0]-i[0]) ** 2+(self.my[1]-i[1]) ** 2)
        sorting = sorted(self.length)
        self.sorting_number = list(set(sorting[:50]))
        
    def recommend_subject(self):
        recommend_subject ={}
        for i in self.sorting_number:
            pos = np.where(np.array(self.length) == i)[0]
            print(pos)
            print(len(pos))
            for j in pos:
                sub = self.recommend['과목명'][j]
                
                if len(recommend_subject) >= 20:
                    break
                elif sub in recommend_subject:
                    recommend_subject[sub] += 1 
                else:
                    recommend_subject[sub] = 1
            if len(recommend_subject) >= 20:
                break   
                
       
        temp = sorted(recommend_subject.items(), key=lambda x: x[1], reverse=True)

        recommend_sub = []
        for i in temp:
            recommend_sub.append(i[0])
        return recommend_sub
    
class Load:
     def __init__(self, major):
        self.subject_load = pd.read_excel('subjects.xlsx')
        self.subject = pd.read_excel('로드계산.xlsx')
        self.total_subject = pd.read_csv('total_subjects.csv')
        self.df = []
        self.factors = {}
        self.subs  = {}
        self.ideal_load = {}
        self.major_id = {'무은재학부':"MOEN", '화학공학과':"CHEB", '신소재공학과':"AMSE", '화학과':"CHEM", '생명과학과':"LIFE", 'IT융합공학과':"CITE", '산업경영공학과':"IMEN", '컴퓨터공학과':"CSED", '수학과':"MATH",'전자전기공학과':"EECE", '물리학과':"PHY", '기계공학과':"MECH"}  
        self.id_ = self.major_id[major]

        for i in range(len(self.total_subject["과목명"])):
            self.ideal_load[self.total_subject["과목명"][i]] = self.total_subject["신청학점"][i]   
        self.corr_column_names = ['정원', '수강인원','응답인원','강의비율','참여비율','영어강의척도비율',
                     '평점','수업조직',	'수업진행',	'동기부여',	'시험',	'학습결과',	'학생만족',	'실험',	'영어강의',	'office hour']
        for i in self.corr_column_names:
            self.factors[i] = abs(np.corrcoef(self.subject['로드'], self.subject[i])[0, 1])
        self.factors = sorted(self.factors.items(), key = lambda item: item[1], reverse = True)

            
        self.learning()
    
     def learning(self):
         x = self.subject[['office hour', '시험', '학생만족', '영어강의척도비율', '평점', '실험', '참여비율', '강의비율', '수업진행', '수업조직']]
         y = self.subject[['로드']]
         sc = StandardScaler()
         sc.fit(x)
 
         x_std = sc.transform(x)

         lin = LinearRegression()
         lin.fit(x_std, y)
         svm_model = SVC(kernel='rbf', C=8, gamma=0.7)
     
         svm_model.fit(x_std, y.values.ravel())
    
    
         x_load = self.subject_load[['office hour', '시험', '학생만족', '영어강의척도비율', '평점', '실험', '참여비율', '강의비율', '수업진행', '수업조직']]
    
         sc = StandardScaler()
         sc.fit(x_load)
     
         x_load_std = sc.transform(x_load)
         svm_y = svm_model.predict(x_load_std).flatten()
         lin_y = lin.predict(x_load_std).flatten()
         self.y_load = (np.array(svm_model.predict(x_load_std))+np.array(lin_y))/2
         
     def load_recommend(self):
         real_load = []

         for i in range(len(self.subject_load["교과목명"])):
             try:
                 real_load.append(self.ideal_load[self.subject_load["교과목명"][i]]*(self.y_load[i]+0.5))
             except:
                 real_load.append(0)
                
         
         for i in range(len(self.subject_load)):
             string = self.subject_load["학수번호"][i]
             if self.id_ in string and int(re.sub(r'[^0-9]', '', string)) < 400: 
                 sub = str(self.subject_load["교과목명"][i])+"_"+str(self.subject_load["교수명"][i])
                 if sub in self.subs:
                     self.subs[sub] = (self.subs[sub] + real_load[i])/2
                 else:
                     self.subs[sub] = real_load[i]
        
         self.subs = sorted(self.subs.items(), key = lambda item: item[1], reverse = True)
        
         return self.subs
    

class Good_grade:
     def __init__(self, major, goal):
        self.goal_grade = goal
        self.subject = pd.read_excel('grade(2022).xlsx')
        

        self.major_id = {'무은재학부':"MOEN", '화학공학과':"CHEB", '신소재공학과':"AMSE", '화학과':"CHEM", '생명과학과':"LIFE", 'IT융합공학과':"CITE", '산업경영공학과':"IMEN", '컴퓨터공학과':"CSED", '수학과':"MATH",'전자전기공학과':"EECE", '물리학과':"PHY", '기계공학과':"MECH"}  
        self.my_sub_num = self.major_id[major]
        
        self.raw_sub_num = np.array(self.subject["학수번호"])
        
        self.goal_split()

        
    
     def goal_split(self):
         self.sub_num = []
         for i in self.raw_sub_num:
             sub = i.split('-')[0]
             if sub in self.sub_num:
                 continue
             else:
                 self.sub_num.append(sub)
        
         subject_grade = {}
         self.sub_name = {}
         subject_grade_4_3 = {}
         subject_grade_4_0 = {}
         subject_grade_3_7 = {}
         subject_grade_3_3 = {}
         subject_grade_3_0 = {}
        
         for i in self.sub_num:
             subject_grade[i] = np.array([float(0)]*19)
        
         for i in self.subject.iloc():
             if i["학수번호"].split('-')[0] in self.sub_name:
                 continue
             else:
                 self.sub_name[i["학수번호"].split('-')[0]] = i["교과목"]
        
         for i in self.subject.iloc():
             subject_grade[i["학수번호"].split('-')[0]] += np.array([i["A+"],i["A0"],i["A-"],i["B+"],i["B0"],i["B-"],i["C+"],i["C0"],i["C-"],i["D+"],i["D0"],i["D-"],i["F"],i["S"],i["U"],i["SA"],i["W"],i["I"],i["GPA계산인원"]])  
        
         for i in self.sub_num:
             if subject_grade[i][-1] == 0:
                 subject_grade_4_3[i] = 0
                 subject_grade_4_0[i] = 0
                 subject_grade_3_7[i] = 0
                 subject_grade_3_0[i] = 0
             else:
                 subject_grade_4_3[i] = subject_grade[i][0]/subject_grade[i][-1]
                 subject_grade_4_0[i] = (subject_grade[i][0]+subject_grade[i][1])/subject_grade[i][-1]
                 subject_grade_3_7[i] = (subject_grade[i][0]+subject_grade[i][1]+subject_grade[i][2])/subject_grade[i][-1]
                 subject_grade_3_3[i] = (subject_grade[i][0]+subject_grade[i][1]+subject_grade[i][2]+subject_grade[i][3])/subject_grade[i][-1]
                 subject_grade_3_0[i] = (subject_grade[i][0]+subject_grade[i][1]+subject_grade[i][2]+subject_grade[i][3]+subject_grade[i][4])/subject_grade[i][-1]
        
        
         self.subject_grade_4_3 = sorted(subject_grade_4_3.items(), key = lambda item: item[1], reverse = True)
         self.subject_grade_4_0 = sorted(subject_grade_4_0.items(), key = lambda item: item[1], reverse = True)
         self.subject_grade_3_7 = sorted(subject_grade_3_7.items(), key = lambda item: item[1], reverse = True)
         self.subject_grade_3_3 = sorted(subject_grade_3_3.items(), key = lambda item: item[1], reverse = True)
         self.subject_grade_3_0 = sorted(subject_grade_3_0.items(), key = lambda item: item[1], reverse = True)
    
     def recommend(self):
         subjects = []
         if self.goal_grade > 4:
            for i in self.subject_grade_4_3:
                if self.my_sub_num in i[0]:
                    subjects.append(str(self.sub_name[i[0]]) + str(i[1]*100) +"%로 목표학점을 위한 학점을 준다")
                    
         elif self.goal_grade > 3.7:
             for i in self.subject_grade_4_0:
                 if self.my_sub_num in i[0]:
                     subjects.append(str(self.sub_name[i[0]]) + str(i[1]*100) +"%로 목표학점을 위한 학점을 준다")
                
         elif self.goal_grade > 3.3:
             for i in self.subject_grade_3_7:
                 if self.my_sub_num in i[0]:
                     subjects.append(str(self.sub_name[i[0]]) + str(i[1]*100) +"%로 목표학점을 위한 학점을 준다")
                
         elif self.goal_grade > 3.0:
             for i in self.subject_grade_3_3:
                 if self.my_sub_num in i[0]:
                     subjects.append(str(self.sub_name[i[0]]) + str(i[1]*100) +"%로 목표학점을 위한 학점을 준다")
                    
         else: 
             for i in self.subject_grade_3_0:
                 if self.my_sub_num in i[0]:
                     subjects.append(str(self.sub_name[i[0]]) + str(i[1]*100) +"%로 목표학점을 위한 학점을 준다")
         return subjects




form_class = uic.loadUiType("ugrp.ui")[0]
  
class MyWindow(QMainWindow, form_class):
     def __init__(self):
         super().__init__()
         self.setupUi(self)
         self.major = "화학과"
         self.goal = 3.3
         self.year = 3
         self.majors = ['무은재학부', '화학공학과', '신소재공학과', '화학과', '생명과학과', 'IT융합공학과', '산업경영공학과', '컴퓨터공학과', '수학과','전자전기공학과', '물리학과', '기계공학과']
         self.Major_set()
         
         self.recommend = Recommend(self.year, self.major)
         self.Goodgrade = Good_grade(self.major, self.goal)
         self.load = Load(self.major)

         self.person_info.clicked.connect(lambda: self.apply_person_info())
         self.start.clicked.connect(lambda: self.start_recommend())
         
     def Major_set(self):
         for i in self.majors:
             self.Major.addItem(i)
     def apply_person_info(self):
         self.major = str(self.Major.currentText())
         self.goal = float(self.goal_grade.value())
         self.year = 2023 - int(self.fresh_year.value())
         self.set_recommend()
         print(self.major, self.goal, self.year)
 
     def set_recommend(self):
         self.recommend = Recommend(self.year, self.major)
         self.Goodgrade = Good_grade(self.major, self.goal)
         self.load = Load(self.major)
         
     def start_recommend(self):
         recommend_list = self.recommend.run_recommend()
         load_list = self.load.load_recommend()
         good_grade_list = self.Goodgrade.recommend()
         
         
         model1 = QStandardItemModel()
         for i in recommend_list:
             model1.appendRow(QStandardItem(i))
         self.recommend_view.setModel(model1)
         
         model2 = QStandardItemModel()
         for i in load_list:
             temp = str(i[0]) + " " +str(i[1])
             model2.appendRow(QStandardItem(temp))
         self.load_view.setModel(model2)
         
         model3 = QStandardItemModel()
         for i in good_grade_list:
             
             model3.appendRow(QStandardItem(i))
         self.good_grade_view.setModel(model3)
         
         
         
     
 # QApplication 객체 생성 및 이벤트 루프 생성 코드
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
























    
















