"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'role', 'height', 'foot_size']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return confirm_password

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class LoginUserForm(AuthenticationForm):
    class Meta:
        fields = ['email', 'password']

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['organizer_name', 'organizer_type']

class GearForm(forms.ModelForm):
    class Meta:
        model = Gear
        fields = ['gear_name', 'gear_type', 'size', 'organizer']

class DiveComputerForm(forms.ModelForm):
    class Meta:
        model = DiveComputer
        fields = ['depth', 'dive_time']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_name', 'country', 'description', 'places', 'organizer']

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['group', 'dive_computer', 'activity', 'gear']
