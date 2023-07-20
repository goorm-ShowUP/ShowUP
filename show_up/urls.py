from django.urls import path

from.import views

urlpatterns = [
    path('', views.index, name='index'),
    path('choosearea/', views.show_area, name='show_area')
]