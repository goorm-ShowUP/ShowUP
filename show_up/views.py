from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from openpyxl import load_workbook
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import datasets, model_selection
from lightgbm import LGBMClassifier
from sklearn.metrics import f1_score,accuracy_score
import joblib

from show_up.models import Show

def index(request):
    excel_to_db()
    return render(request,'index.html')



def predict(request):
    
    # lightgbm 모델 불러오기
    model = joblib.load(open('lightgbm.pkl', 'rb'))
    
    # 모델 사용해서 클러스터 예측하기(괄호안에 DateFrame 형태로 넣으면 클러스터 반환함)
    # print(model.predict())   
    
# def choose_area(request):
#     return

def show_area(request):
    
    공연전체데이터 = pd.read_excel('media/clustering.xlsx')
    해당클러스터공연 = 공연전체데이터[공연전체데이터['clusters16']==7]
    area_list = 해당클러스터공연['지역(시도)'].unique().tolist()
    print(area_list)
    context={'area_list': area_list}
    return render(request,'select_area.html',context)


def excel_to_db():
    공연전체데이터s = pd.read_excel('media/clustering.xlsx')
    공연전체데이터 = pd.DataFrame(공연전체데이터s)
    ss=[]
    for i in range(len(공연전체데이터)):
        
        st = (공연전체데이터['공연명'][i], 공연전체데이터['공연시설명'][i], 공연전체데이터['지역(시도)'][i], 공연전체데이터['지역(구군)'][i], 공연전체데이터['장르'][i], 공연전체데이터['첫가격'][i], 공연전체데이터['공연관람연령'][i], 공연전체데이터['공연 런타임'][i], 공연전체데이터['공연기간(일수)'][i], 공연전체데이터['clusters16'][i])
        ss.append(st)
    for i in range(len(공연전체데이터)):
        print(ss[i])
        Show.objects.create(showname=ss[i][0], concerthall=ss[i][1], sido=ss[i][2], gugun=ss[i][3], genre=ss[i][4], price=ss[i][5], age=ss[i][6], runtime=ss[i][7], period=ss[i][8], cluster=ss[i][9])
