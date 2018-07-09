from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LightSaltUserCreationForm, LightSaltPastorCreationForm
from .models import LightSaltPastor, LightSaltUser

# class SignUpView(View):
#     form_class = LightSaltUserCreationForm
#     initial = {'key': 'value'}
#     template_name = 'registration/sign_up.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/accounts/login')
#         return render(request, self.template_name, {'form': form})


## 유저 생성
class UserCreateView(CreateView):
    model = LightSaltUser
    form_class = LightSaltUserCreationForm
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
    form_class = LightSaltUserCreationForm
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