from django import forms
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from foodexpress_app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, label="Пароль")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        user = auth.authenticate(request=self.request, **self.cleaned_data)
        if user is None:
            raise ValidationError({'password': 'Неправильный пароль или имя пользователя'})


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, label="Пароль")
    password_check = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
    email = forms.EmailField(label="Почта")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            raise ValidationError({'password': 'Passwords do not match', 'password_check': ''})

    def save(self, **kwargs):
        data = self.cleaned_data

        data.pop('password_check')

        user = User.objects.create_user(**data)
        if not user:
            self.add_error(None, "User saving error!")
            return None
        profile = Profile.manager.create(user=user)
        if not profile:
            self.add_error(None, "Profile saving error!")
            return None

        return user


class SettingsForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин")
    address = forms.CharField(required=False, label="Адрес", disabled=True)
    email = forms.EmailField(required=False, label="Почта")
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, label="Предыдущий пароль")
    new_password = forms.CharField(min_length=4, widget=forms.PasswordInput, label="Новый пароль", required=False)
    password_check = forms.CharField(widget=forms.PasswordInput, label="Повторите новый пароль", required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean_password_check(self):
        new_password = self.cleaned_data['new_password']
        password_for_checking = self.cleaned_data['password_check']
        if password_for_checking != new_password:
            raise ValidationError("Passwords don't match!")
        return password_for_checking

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(request=self.request, username=username, password=password)
        if user is None:
            raise ValidationError("The old password is incorrect!")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)

        username = self.cleaned_data.get('username')
        new_password = self.cleaned_data.get('new_password')

        profile = user.profile
        user.save()
        profile.save()

        if new_password:
            user.set_password(new_password)
            user.save()

            test_auth_user = auth.authenticate(request=self.request, username=username, password=new_password)
            if test_auth_user is not None:
                login(self.request, test_auth_user)
            else:
                self.add_error(None, "User authentication error!")

        return user