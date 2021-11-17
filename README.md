# Esp-32-home-automation-with-telegram-chatbot-
Creating Esp 32 home automation that can be controlled by either web interface or telegram chat bot


## steps:
 * NOTE: the ESP 32 circuit is not yet available *
 
Create new folder for your project.
Then in the project folder open the terminal
create a virtual environment using for the project;

        python3 pip -m venv <virtual environment name>
 activate the virtual environment by:
       **source <virtual environment name>/bin/activate**
       
then install the following python package:-

        django (pip install django==2.2.16)
        telebot
        request(pip install request)
        schedule(pip install schedule)
            
 with active virtual environment make your project;
 
        django-admin startproject <project name>
          
create your django app:

        run: django-admin startapp <app name>

after succefully creating django project and app
 **in the app folder**: add [url.py](/url.py) and [forms.py](/forms.py)
 In the root directory. Create following folders,
**static -> this holds the static files such as css,js and images** and 
**Templates -> this holds all html files**
 In the root directory of your project(the folder containing manage.py file) go to the project file
  add the urlpatterns from the url.py(__The file will be provided later__) 
 and change settings.py file as below:
 
          add your app name in INSTALLEDAPPS list ->"<app name>"
          add "'DIRS': [BASE_DIR,"Templates"]," in TEMPLATES list
          add this statement at the end of setting file
              (
                  STATIC_URL = '/static/'
                  STATICFILES_DIRS=[os.path.join(BASE_DIR,'static'),])

      add url.py file(copy the urlpattern in the from url.py)
                            

**Some of the default django files are not provided here**

For the page to have ability to run remotely: i used [ngrok](https://ngrok.com) service for tunnelling
download and extract ngrok from their official site to allow you to give your device 
internet capabilities. Then run the django sever after setting most parameter are set and not the port at which the is listening
    run ./ngrok<port from sever from django>

For telegram chatbot:
Go to telegram->serach->**@botFather**->start-> follow the procedures to create the bot

Note the bot token because it is very important when you what to control your bot

  **__add .env file that will contain the bot key in format: "KEY=[bot token]"__**
  
You can adjust the time at which the bot run in schedule then run the run_bot.py, 
