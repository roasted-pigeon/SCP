import django.forms

from .models import User, Game
from django.forms import ModelForm

class DateInput(django.forms.DateInput):
    input_type = 'date'

class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password_hash']

    widgets = {
        'email': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        ),
        'password_hash': django.forms.TextInput(
            attrs={
                'class':'input'
            }
        )
    }

class UserSignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password_hash']

    widgets = {
        'first_name': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        ),
        'last_name': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        ),
        'email': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        ),
        'password_hash': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        )
    }
    password_repeat = django.forms.CharField(widget=django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        )
    )

class GameCreateForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'next_session_date']

    widgets = {
        'title': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        ),
        'description': django.forms.TextInput(
            attrs={
                'class': 'input'
            }
        ),
        'next_session_date': DateInput(),
    }

