from django import forms
from .models import Utilisateur


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-input',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input',
            'required': True,
        })
    )


class RegisterForm(forms.Form):
    nom_complet = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full name',
            'class': 'form-input',
            'required': True,
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-input',
            'required': True,
        })
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number',
            'class': 'form-input',
        })
    )
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password (min 6 chars)',
            'class': 'form-input',
            'required': True,
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-input',
            'required': True,
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class FlightSearchForm(forms.Form):
    departure = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. CDG - Paris',
            'list': 'airports-departure',
            'required': True,
        })
    )
    destination = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. DLA - Douala',
            'list': 'airports-arrival',
            'required': True,
        })
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'required': True,
        })
    )
    passagers = forms.IntegerField(
        min_value=1,
        max_value=9,
        initial=1,
        widget=forms.HiddenInput()
    )
    children = forms.IntegerField(
        min_value=0,
        max_value=9,
        initial=0,
        widget=forms.HiddenInput()
    )
    flight_class = forms.ChoiceField(
        choices=[
            ('economique', 'Economy'),
            ('business', 'Business'),
            ('premiere', 'First Class'),
        ],
        initial='economique',
    )
