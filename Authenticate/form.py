from django import forms
from django.forms import models
from django.core.validators import RegexValidator
# from .models import Users

class Signupform(forms.Form):
    #customized validators
    passwordRegex=RegexValidator(regex=r"[\d+\w{4,6}][@#$%&\+]")
    numberRegex=RegexValidator(regex=r"\+\d{1,13}")

    username=forms.CharField(max_length=80)
    telegram_username=forms.CharField(max_length=80,required=False)
    password=forms.CharField(widget=forms.PasswordInput(),validators=[passwordRegex])
    
    phone_number=forms.CharField(validators=[numberRegex],max_length=15,label='phone number for telegram',required=False)
    maincontrollerID=forms.IntegerField(required=True)


class Signupaddedform(Signupform):
    maincontrollerID=forms.IntegerField(required=False)
    verification_id=forms.CharField(max_length=20,required=True)



class Loginform(forms.Form):
    username=forms.CharField(max_length=80)
    password=forms.CharField(widget=forms.PasswordInput())


class adddeviceform(forms.Form):
    device_name=forms.CharField(max_length=20)
    pin_number=forms.IntegerField(label="GPIO pin the device is connected")



class addduserform(forms.Form):
    added_username=forms.CharField(max_length=80,required=True)
    added_username2=forms.CharField(max_length=80,required=True)

class edit_user_details(Signupform):
    passwordRegex=RegexValidator(regex=r"[\d+\w{4,6}][@#$%&\+]")
    numberRegex=RegexValidator(regex=r"\+\d{1,13}")

    username=forms.CharField(max_length=80)
    telegram_username=forms.CharField(max_length=80,required=False)
    password=forms.CharField(widget=forms.PasswordInput(),validators=[passwordRegex])
    phone_number=forms.CharField(validators=[numberRegex],max_length=15,label='phone number for telegram',required=False)
    