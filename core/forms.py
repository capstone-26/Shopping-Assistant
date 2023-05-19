from .models import *
from django import forms

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')


# class ProfileForm(forms.ModelForm):
#     birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     class Meta:
#         model = Profile
#         fields = ('bio', 'location', 'birthdate')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
        }


class ProfileForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
        label='Birthdate',
        help_text='Select your birthdate'
    )

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birthdate')
        labels = {
            'bio': 'Bio',
            'location': 'Location',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Bio'}),
            'location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Location'}),
        }
