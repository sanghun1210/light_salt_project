from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, UserCreationForm, LightSaltPastorCreationForm, SettingsUserUpdateForm
from .models import LightSaltPastor, LightSaltUser
from django.conf import settings

from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login)

# 로그인
class UserLoginView(DjangoLoginView):
    form_class = UserLoginForm
    template_name = 'account/login.html'

## 유저 생성
class UserCreateView(FormView):
    model = LightSaltUser
    form_class = UserCreationForm
    template_name = 'account/user_create.html'

    def form_valid(self, form):
        user = form.save()
        return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
        # return super().form_valid(form)

## 유저 확인 및 수정
class UserDetailView(LoginRequiredMixin, DetailView):
    model = LightSaltUser
    template_name = 'account/user_detail.html'

    def form_valid(self, form):
        return super(UserDetailView, self).form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = LightSaltUser
    form_class = UserCreationForm
    template_name = 'account/user_update.html'

    def get_object(self):
        return self.request.user

## 유저 목록
class UserListView(ListView): 
    model = LightSaltUser
    template_name = 'account/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self): 
        queryset = super(UserListView, self).get_queryset()
        q = self.request.GET.get("q") 
        if q: 
            # Return a filtered queryset 
            return queryset.filter(title__icontains=q)
        return queryset
    
class PastorActionMixin(object):
    @property
    def action(self):
        msg = "{0} is missing action.".format(self.__class__)
        raise NotImplementedError(msg)

    def form_valid(self, form):
        msg = "Pastor {0}!".format(self.action)
        messages.info(self.request, msg)
        return super(PastorActionMixin, self).form_valid(form)

class PastorCreateView(LoginRequiredMixin, TemplateView):
    model = LightSaltPastor
    action = "created"
    template_name = 'account/church_config.html'

class PastorDetailView(LoginRequiredMixin, DetailView):
    model = LightSaltPastor

class SettingsUserInformationView(LoginRequiredMixin, FormView):
    model = LightSaltUser
    action = "created"
    form_class = SettingsUserUpdateForm
    template_name = 'account/settings_user_information.html'

class SettingsUserPasswordView(LoginRequiredMixin, TemplateView):
    model = LightSaltPastor
    action = "created"
    template_name = 'account/settings_user_password.html'

class SettingsChurchInformationView(LoginRequiredMixin, TemplateView):
    model = LightSaltPastor
    action = "created"
    template_name = 'account/settings_church_information.html'