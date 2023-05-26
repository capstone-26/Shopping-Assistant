from .models import *
from django import forms

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
        help_text='Select your birthdate',
        required=False  # Set required attribute to False
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['location'].required = False


class PasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input', 'placeholder': 'Old Password'}),
        label='Old Password'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input', 'placeholder': 'New Password'}),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError(
                "New password and confirm password do not match.")

        return cleaned_data
