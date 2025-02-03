from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name = 'home'),
 
    # path('login/', loginPage, name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),

    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),

    path('profile/<int:pk>/', userProfile, name = 'user-profile'),
    path('update-user/', updateUser, name = 'update-user'),    

    path('room/<int:pk>/', room, name = 'room'),
    path('create-room/', createRoom, name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom, name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom, name = 'delete-room'),

    path('delete-message/<int:pk>/', deleteMessage, name = 'delete-message'),    
    path('delete-user/<int:pk>/', deleteProfile, name = 'delete-profile'),    

    path('topics/', topicsPage, name='topics'),
    path('activity/', activityPage, name='activity'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'home/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = "home/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'home/password_reset_complete.html'), name='password_reset_complete'),


]