from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,PasswordResetCompleteView,
    PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView
)

app_name = 'profiles'

urlpatterns = [
    path('login/',LoginView.as_view(template_name='accounts/main_login.html'),name="login"),
    path('logout/', LogoutView.as_view(template_name='accounts/main_logout.html'),name="logout"),
    path('signup/', views.register,name="register"),
    path('myprofile/',views.my_profile_view,name='my-profile-view' ),
    path('followers/',views.my_followers_list_view,name='my-follower-list-view'),
    path('youfollow/',views.you_follow_list_view,name='you-follow-list-view'),
    path('all_users_view/',views.all_users_list_view,name='all-users-list-view'),
    path('profile_view/',views.view_profile_view,name='profile-view'),
    path('specific_profile_view/',views.specific_profile_view,name='specific-profile-view'),
    path('follow_unfollow/',views.follow_unfollow_view,name='follow-unfollow-view'),
]

#http://127.0.0.1:8000/profiles ->main url.py
#http://127.0.0.1:8000/profiles/myprofile ->main url.py
