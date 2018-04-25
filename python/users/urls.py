from django.urls import path

from users import views


app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('guest/', views.guest, name='guest'),
    path('logout/', views.user_logout, name='logout'),
]
