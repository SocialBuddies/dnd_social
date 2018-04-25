from django.urls import path

from npcs import views


app_name = 'npcs'
urlpatterns = [
    path('create/', views.create_npc, name='create_npc'),
]
