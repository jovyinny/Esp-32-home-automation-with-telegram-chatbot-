from re import U
from django.core import validators
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField

# Create your models here.


# list of connected devices, maincontrollerID, pin numbers and current status
class Connected_devices(models.Model):
    MaincontrollerID=CharField(max_length=50,null=True)
    Device_name=models.CharField(max_length=30,null=True)
    Pin_number=models.PositiveIntegerField(null=True)
    Current_status=models.BooleanField(null=True)


# list of all maincontrollers and number of connected devices
class Maincontroller(models.Model):
    MaincontrollerID=models.CharField(max_length=50,unique=True)
    # Number_of_devices=models.PositiveIntegerField(null=True,blank=True)
    Connected_devices_list=models.ForeignKey(Connected_devices,on_delete=CASCADE,null=True,blank=True)


# git repository:https://github.com/jovyinny/Esp-32-home-automation-with-telegram-chatbot-.git


# list of registered users and their particulars
class Users(models.Model):
    Name=models.CharField(max_length=50)
    Telegram_username=models.CharField(max_length=50,null=True,blank=True,unique=True)
    # custom validators
    passwordRegex=RegexValidator(regex=r"[\d+\w{4,6}][@#$%&\+]") #password validator pattern
    numberRegex=RegexValidator(regex=r"^\+\d{1,13}") #phone number validator pattern
    
    Password=models.CharField(validators=[passwordRegex],max_length=20, null=True,help_text="password should start with atleast 4 letters or atleat one digit and followed by atleast one special characters such as (@#$%&+)")
    Level=models.CharField(max_length=10,default='subuser')
    Phone_number=models.CharField(validators=[numberRegex],max_length=15,null=True,unique=True)
    MaincontrollerID=models.ForeignKey(Maincontroller,on_delete=CASCADE,verbose_name="MaincontollerID")
    Verification_id=models.CharField(max_length=20,null=True,blank=True)