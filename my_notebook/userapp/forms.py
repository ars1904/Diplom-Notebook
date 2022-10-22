

from django.contrib.auth.forms import UserCreationForm
from .models import NoteUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = NoteUser
        fields = ('username', 'password1', 'password2', 'email')