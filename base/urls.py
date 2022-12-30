from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('', views.home, name="home"),
    path('profile/<int:id>/', views.user_profile, name="profile"),
    path('group/<int:id>/', views.group, name="group"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<int:id>/', views.update_room, name='update-room'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('delete-message/<int:id>/', views.delete_message, name='delete-message'),
    path('update-user/', views.update_user, name='update-user'),
    path('topics/', views.topics_page, name='topics'),
    path('activities/', views.activity_page, name='activities')
]