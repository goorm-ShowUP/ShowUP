from django.urls import path

from.import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('index3/', views.index3, name='index3'),path('index4/', views.index4, name='index4'),path('index5/', views.index5, name='index5'),path('index6/', views.index6, name='index6'),
]