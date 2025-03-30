from django.urls import path, include
from .views import (
    RegisterView, LoginView, ProfileView,
    follow_user, unfollow_user, get_followers, get_following
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('followers/', get_followers, name='get-followers'),
    path('following/', get_following, name='get-following'),
]