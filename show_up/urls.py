from django.urls import path

from.import views

urlpatterns = [
     path('', views.index, name='index'),
     path('choosearea/', views.show_area, name='show_area'),
    path('choosearea/<s_cluster>/<s_area>/', views.show_area_concerthall, name='show_area_concerthall')
]