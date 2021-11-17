from telegram.ext import Updater,commandhandler
from dotenv import load_dotenv
import os,sys,django
import telebot
from telegram import ParseMode
import urllib.request

sys.path.append('/media/jovine/Mutelani/Practice/Python/Library/Home_Automation')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Home_Automation.settings'
django.setup()

from Authenticate.models import Connected_devices,Users

# loading api key from hidden file
load_dotenv()
key=os.getenv('KEY')

bot=telebot.TeleBot(key)

def get_bot_url():
    url="https://api.telegram.org/bot{}/".format(key)
    return url

# print(get_bot_url())

def start():
    text="\nThis bot is created for Home Automation(JBM Home Automation)\nThe user who has officially registered can use his/her telegram number provided during sign up\n"
    text2="The commmand that  bot can handle are:\n /help or /start    -> To get info on how to use the bot\n/<device name> on or off  -> This turns on or off  named device\n /device_info  -> This returns info about all connected devices"    
    combined_text=text+text2
    return combined_text



@bot.message_handler(commands=['help'])
def help(message):
    pass
    text=start()
    bot.reply_to(message,text)



def check_sent_text(text,username):
    print(text)
    if 'start' in text.lower() or 'help' in text.lower():
        return start()
    elif 'on' in text.lower() or 'off' in text.lower():
        return device_on_or_off(text,username)
    elif 'device info' in text or 'info' in text.lower():
        return device_info(username)
    
    elif 'schedule' in text.lower():
       
        return 'False'
        pass
    else:
        text='Sorry, Unrecognized text'
        return text



def return_string(mylist):
    new_string=''
    lenght=len(mylist)
    for i in range(len(mylist)):
        if i ==(lenght-1):
            new_string+=mylist[i]
        else:
            new_string+=mylist[i]
            new_string+=" "       
    return new_string


def device_on_or_off(text,username):
    text=text.split()
    status=text[-1].lower()
    device_name=text[0:-1]
    if device_name==[]:
        text="Device name unrecognized"
        return text
    else:
        try:
            user_obj=Users.objects.get(Telegram_username=username)
            if (user_obj):
                maincontrollerID=user_obj.MaincontrollerID.MaincontrollerID
                if maincontrollerID:
                    device_name=return_string(device_name)
                    device=Connected_devices.objects.get(MaincontrollerID=maincontrollerID,Device_name=device_name)
                    status="True" if status=="on" else "False"
                    device.Current_status=status
                    device.save()
                    status="on" if status=="True" else "off"
                    text=f"{device_name} is now {status}"
                    return text
                else:
                    text="Sorry,The device is unrecognized"
            else:
                text="Sorry,Your telegram username unmatched"

        except Exception as error:
            text="Sorry,The device is unrecognized or\nYour telegram username unmatched"
            print(error,"occurred in device_on_or_off at functions_bot")

        return text


def device_info(username):
    try:
        user_obj=Users.objects.get(Telegram_username=username)
        if (user_obj):
            maincontrollerID=user_obj.MaincontrollerID.MaincontrollerID
            if maincontrollerID:
                device=Connected_devices.objects.filter(MaincontrollerID=maincontrollerID).values()
                device_details=""
                for i in device:
                    status= "on" if i["Current_status"] == True else "off"
                    device_details+=f"{i['Device_name']} is {status}\n" 

        return device_details

    except Exception as error:
        text="Sorry,Your telegram username unmatched"
        print(f"{error}occurred in device_on_or_off at functions_bot")

    return text




def connect(host='https://api.telegram.org'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False


