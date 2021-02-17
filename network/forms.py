from django import forms
from django.forms import ModelForm
from .models import Post, User, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from django.contrib.auth import get_user_model

User = get_user_model()


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add new post.."})
    )

    class Meta:
        model = Post
        fields = ["content"]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

