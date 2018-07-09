from django.urls import path
from . import views

urlpatterns = {
    path('', views.media, name='media'),
}
