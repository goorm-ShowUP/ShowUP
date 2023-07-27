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

def indexj(request):
    return render(request,'show_up/index.html')


def price(request):
    return render(request,'show_up/price.html')

def genre(request):
    if request.method == 'POST':
        #int값 외 다른값 들어올 시 처리 해야함
        choice.price = int(request.POST['price'])
        print(request.POST)

    return render(request,'show_up/genre.html')

def runtime(request):
    if request.method == 'POST':
        choice.genre = request.POST['genre']

    return render(request,'show_up/runtime.html')

def day(request):
    if request.method == 'POST':
        choice.runtime = request.POST['runtime']

    return render(request,'show_up/day.html')

def age(request):
    if request.method == 'POST':
        choice.day = request.POST['day']

    return render(request,'show_up/age.html')

def result(request):
    if request.method == 'POST':
        choice.age = request.POST['age']
        
    return render(request,'show_up/result.html',{'choice':choice})

def index(request):
    # excel_to_db()
    predict()
    return render(request,'index.html')

def predict():
    
    # 예시
    # 인덱스 9872행
    sample_df = pd.DataFrame({
    '첫가격' : [80000],
    'genre' : ['대중음악'],
    '공연 런타임' : [130],
    '공연기간(일수)' : [1],
    '공연관람연령' : [14],
    })
    
    genre_df= pd.DataFrame({
        'genre':["대중음악",'무용','뮤지컬','복합','서양음악(클래식)','서커스/마술','연극','한국음악(국악)']
    })
    print(genre_df)
    print(sample_df.iloc[0]['genre'])
    #범주형/연속형 변수 분리
    con_col = ['price','runtime','period','age']
    # cat_col = ['genre']
    
    #get_dummies()로 범주형 변수 원핫인코딩
    g = pd.get_dummies(sample_df.iloc[0]['genre'], columns=genre_df['genre'], drop_first=True)
    print(g)
    # scaler 불러오기
    scaler = joblib.load(open('scaler.pkl', 'rb'))
    
    # sample_df.loc[:,con_col] = scaler.transform(sample_df.loc[:,con_col])
    # print(sample_df)
    
    
    # lightgbm 모델 불러오기
    # model = joblib.load(open('lightgbm.pkl', 'rb'))
    
    # 모델 사용해서 클러스터 예측하기(괄호안에 DateFrame 형태로 넣으면 클러스터 반환함)
    # print(model.predict())   
    
# def choose_area(request):
#     return

def show_area(request):
    
    shows = Show.objects.filter(cluster=7)
    공연데이터 = pd.DataFrame(list(shows.values()))
    area_list = 공연데이터['sido'].unique().tolist()
    print(area_list)
    context={'area_list': area_list,'cluster':7}
    return render(request,'select_area.html',context)

def show_area_concerthall(request,s_cluster,s_area):
    shows = Show.objects.filter(cluster=s_cluster,sido=s_area)
    공연장데이터 = pd.DataFrame(list(shows.values()))
    concerthall_list = 공연장데이터['concerthall'].unique().tolist()
    print(concerthall_list)
    context={'concerthall_list': concerthall_list}
    return render(request,'show_concerthall.html',context)

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