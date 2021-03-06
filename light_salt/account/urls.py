from django.urls import path
from django.conf.urls import url
from .views import (PastorCreateView, PastorDetailView, UserCreateView, UserDetailView, UserUpdateView, 
                    UserListView, UserLoginView, SettingsUserInformationView, SettingsUserPasswordView, SettingsUserInformationView)

urlpatterns = [
    path('sign-up/', UserCreateView.as_view(), name='sign_up'), #사용자 등록
    path('sign-in/', UserLoginView.as_view(), name='login'),

    path('user-detail/', UserDetailView.as_view()),
    path('user-update/', UserUpdateView.as_view()),
    path('users/', UserListView.as_view(), name='users'),
    path('settings/user-information', SettingsUserInformationView.as_view()),
    path('settings/user-password', SettingsUserPasswordView.as_view()),
    path('settings/user-information', SettingsUserInformationView.as_view()),
    path(r"ˆ(?P<pk>\d+)/$", PastorDetailView.as_view(), name='pastor_detail'),
]