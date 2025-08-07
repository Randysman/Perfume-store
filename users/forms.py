from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email')

        image = forms.ImageField(required=False)
        first_name = forms.CharField()
        last_name = forms.CharField()
        username = forms.CharField()
        email = forms.CharField()