from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.conf import settings

from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, UserCreationForm, LightSaltPastorCreationForm
from .models import LightSaltPastor, LightSaltUser
from django.shortcuts import resolve_url


# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        print('#434234324234')
        auth_login(self.request, form.get_user())
        print('tes2222')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        print('ddddd')
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        # redirect_to = self.request.POST.get(
        #     self.redirect_field_name,
        #     self.request.GET.get(self.redirect_field_name, '')
        # )
        # url_is_safe = is_safe_url(
        #     url=redirect_to,
        #     allowed_hosts=self.get_success_url_allowed_hosts(),
        #     require_https=self.request.is_secure(),
        # )
        # return redirect_to if url_is_safe else ''
        return ''

## 유저 생성
class UserCreateView(CreateView):
    model = LightSaltUser
    form_class = UserCreationForm
    template_name = 'account/user_create.html'

    def form_valid(self, form):
        return super(UserCreateView, self).form_valid(form)

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

class PastorCreateView(LoginRequiredMixin, CreateView):
    model = LightSaltPastor
    action = "created"
    form_class = LightSaltPastorCreationForm

class PastorDetailView(LoginRequiredMixin, DetailView):
    model = LightSaltPastor