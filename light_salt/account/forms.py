from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import LightSaltUser, LightSaltPastor

#####################
### 사용자 정보 관리 폼

class LightSaltUserCreationForm(forms.ModelForm):
    member_id = forms.CharField(label="Member Id")
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email", max_length=150)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = LightSaltUser
        fields = ("member_id", "name", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)

        return password2

    def save(self, commit=True):
        user = super(LightSaltUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LightSaltUserChangeForm(forms.ModelForm):
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
