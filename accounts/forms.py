from pyexpat import model
from attr import attr, fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, gender_choice
from datetime import datetime





class ProfileForm(forms.ModelForm):


    first_name = forms.CharField(label="first", required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    gender = forms.ChoiceField(required=True, choices=gender_choice,
                               widget=forms.RadioSelect,
                               )
    cellphone_number = forms.IntegerField(required=True)

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'cellphone_number',
            'gender',
            'avatar',
        ]

    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=4, max_length=10)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            
        return user

