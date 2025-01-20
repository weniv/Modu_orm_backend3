from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        forbidden_words = ["개", "바보", "멍청이"]
        for i in forbidden_words:
            if i in username:
                raise forms.ValidationError(
                    f'유저 이름에 "{i}" 단어를 사용할 수 없습니다.'
                )
        if len(username) < 4:
            raise forms.ValidationError("유저 이름이 너무 짧습니다.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)
