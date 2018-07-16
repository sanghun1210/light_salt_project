from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from .models import LightSaltUser, LightSaltPastor, Believer
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import capfirst

#####################
### 사용자 정보 관리 폼

UserModel = get_user_model()

class UserLoginForm(forms.Form):
    member_id = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder':"ID", 'class':"input is-large"}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':"Password", 'class':"input is-large"}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(member_id)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the label for the "username" field.
        # pk 정의
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

    def clean(self):
        member_id = self.cleaned_data.get('member_id')
        password = self.cleaned_data.get('password')

        #member_id가 pk이므로 
        username = member_id

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'member_id': 'ID'},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class UserCreationForm(forms.ModelForm):
    member_id = forms.CharField(label="Member Id")
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email", max_length=150)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = LightSaltUser
        fields = ("member_id", "name", "email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = LightSaltUser
        fields = ("member_id", "name", "email")        

    def clean_password(self):
        return self.initial["password"]

#####################
### 목사 정보 관리 폼

class LightSaltPastorCreationForm(forms.ModelForm):
    pastor_id = forms.CharField(label="Pastor Id")
    church_name = forms.CharField(label="Church Name")
    church_post = forms.CharField(label="Church Post")
    church_address = forms.CharField(label="Church Address")
    authentication_yn = forms.BooleanField(label="인증 여부")

    class Meta:
        model = LightSaltPastor
        fields = {'pastor_id', 'church_name', 'church_post', 'church_address', 'authentication_yn'}

class LightSaltPastorChangeForm(forms.ModelForm):
    class Meta:
        model = LightSaltPastor
        fields = ("pastor_id", "church_name", "church_post", "church_address", "authentication_yn")


#####################
### 신도 관리 폼

class BelieverCreationForm(forms.ModelForm):
    nick_name = forms.CharField(label="nick_name")
    duty_code = forms.CharField(label="duty_code")
    consult_yn = forms.BooleanField(label="consult_yn")
    board_create_yn = forms.BooleanField(label="board_create_yn")

    member_id = forms.ModelChoiceField(queryset=LightSaltUser.objects.all())
    church_no = forms.ModelChoiceField(queryset=LightSaltPastor.objects.all())

    class Meta:
        model = Believer
        fields = {'nick_name', 'duty_code', 'consult_yn', 'board_create_yn', 'member_id', 'church_no'}

class BelieverChangeForm(forms.ModelForm):
    class Meta:
        model = Believer
        fields = {'nick_name', 'duty_code', 'consult_yn', 'board_create_yn', 'member_id', 'church_no'}
