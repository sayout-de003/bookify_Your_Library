# library/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# library/forms.py


from .models import CreativeWork, Comment

class CreativeWorkForm(forms.ModelForm):
    class Meta:
        model = CreativeWork
        fields = ['title', 'category', 'description', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
