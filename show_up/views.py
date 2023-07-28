from django.http import HttpResponse
from django.shortcuts import render
from .models import Choice
import pandas as pd
import numpy as np

from openpyxl import load_workbook
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import datasets, model_selection
from lightgbm import LGBMClassifier
from sklearn.metrics import f1_score,accuracy_score
import joblib
from show_up.models import Show
choice = Choice()

def index(request):
    return render(request,'show_up/index.html')

def price(request):
    return render(request,'show_up/price.html')

def genre(request):
    if request.method == 'POST':
        #int값 외 다른값 들어올 시 처리 해야함
        choice.price = int(request.POST['price'])

    return render(request,'show_up/genre.html')

def runtime(request):
    if request.method == 'POST':
        choice.genre = request.POST['genre']

    return render(request,'show_up/runtime.html')

def day(request):
    if request.method == 'POST':
        choice.runtime = int(request.POST['runtime'])

    return render(request,'show_up/day.html')

def age(request):
    if request.method == 'POST':
        choice.day = int(request.POST['day'])

    return render(request,'show_up/age.html')

# 사용자 인풋 값 전처리 후 모델 적용해 cluster값 추출
def predict(): 
    # 예시 데이터
    # 인덱스 9872행  => 클러스터 7로 예측해줘야함
    sample_df = pd.DataFrame({
    '첫가격' : [choice.price],
    '장르' : [choice.genre],
    '공연 런타임' : [choice.runtime],
    '공연기간(일수)' : [choice.day],
    '공연관람연령' : [choice.age],
    })
    
    genre_df= pd.DataFrame(
        [[0,0,0,0,0,0,0,0]],
        columns=['장르_대중음악','장르_무용','장르_뮤지컬','장르_복합','장르_서양음악(클래식)','장르_서커스/마술','장르_연극','장르_한국음악(국악)']
    )

    g="장르_"+sample_df['장르'][0]
    genre_df[g][0]=1

    con_col = ['첫가격','공연 런타임','공연기간(일수)','공연관람연령']
    
    scaler = joblib.load(open('scaler.pkl', 'rb'))
    
    sample_df.loc[:,con_col] = scaler.transform(sample_df.loc[:,con_col])
    sample_df=sample_df.drop('장르', axis = 'columns')
    
    df=pd.concat([sample_df,genre_df],axis=1)
    
    # lightgbm 모델 불러오기
    model = joblib.load(open('lightgbm.pkl', 'rb'))
    # 모델 사용해서 클러스터 예측하기(괄호안에 DateFrame 형태로 넣으면 클러스터 반환함)
    cluster=model.predict(df)[0]
    
    return cluster
    

# 해당 클러스터의 공연장 지역 목록 보여주기
def show_area(request):
    
    cluster = predict()

    shows = Show.objects.filter(cluster=cluster)    # 괄호 값 넘어오는 클러스터 값으로 변경 필요
    공연데이터 = pd.DataFrame(list(shows.values()))
    area_list = 공연데이터['sido'].unique().tolist()
    print(area_list)
    context={'area_list': area_list,'cluster':cluster}    # 괄호 값 넘어오는 클러스터 값으로 변경 필요
    return render(request,'select_area.html',context)


# 선택한 지역들의 공연장 목록 보여주기
def show_area_concerthall(request,s_cluster,s_area):
    shows = Show.objects.filter(cluster=s_cluster,sido=s_area)
    공연장데이터 = pd.DataFrame(list(shows.values()))
    concerthall_list = 공연장데이터['concerthall'].unique().tolist()
    print(concerthall_list)
    context={'concerthall_list': concerthall_list}
    return render(request,'show_concerthall.html',context)




# 엑셀데이터 db저장
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