from django.urls import path
from django.conf.urls import url
from .views import PastorCreateView, PastorDetailView, UserCreateView, UserDetailView, UserUpdateView, UserListView

urlpatterns = [
    # url('sign-up/', SignUpView.as_view()),
    url('sign-up/', UserCreateView.as_view()),
    url('user-detail/', UserDetailView.as_view()),
    url('user-update/', UserUpdateView.as_view()),
    url('users/', UserListView.as_view(), name='users'),
    url('pastor-create/', PastorCreateView.as_view(), name='pastor_create'),
    url(r"ˆ(?P<pk>\d+)/$", PastorDetailView.as_view(), name='pastor_detail'),
]