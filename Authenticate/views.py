from django.shortcuts import render
from Authenticate.form import *
from django.http import HttpResponseRedirect
from .functions import generate_verification_id,string_no_space_dict
from .functions import User,MainUser,SubUser,Devices

# Create your views here.

#index/login page view... handling logins
def index(request):
    try:
        login_form=Loginform()#form from django form that displays in default
        message='Login please' 
        if request.method == 'POST':
            login_form=Loginform(request.POST)

            if login_form.is_valid():
                username=request.POST['username']
                password=login_form.cleaned_data['password']
                # print(get_user_password(username),"login")
                logging_user=User(username)
                device_obj=Devices('none')
                if password==logging_user.get_user_password(username):

                    #setting session keys and values after a succeful login...
                    # this will help prevent unauthorized actions
                    request.session['username']=username
                    request.session['id']=device_obj.get_maincontroller(username)
                    request.session['is_logged_in']=True
                    request.session['level']=logging_user.is_user_main_level(username)

                    # print(logging_user.get_user_level(username),"in index")
                    return HttpResponseRedirect('home',{'username':username})
                else:
                    message="Wrong creditials entered"
        else:
            login_form=Loginform()
        
        context={'username':login_form['username']
                ,'password':login_form['password'],"message":message}

        return render(request,"login.html",context)
    except Exception as expt:
        print(f"{expt} occured at index in views")


# main user sign up view
def signup(request):
    try:
        signup_form=Signupform()
        message=''
        if request.method == 'POST' and request.session['is_logged_in']:
            signup_form=Signupform(request.POST)
            if signup_form.is_valid():
                # print(signup.cleaned_data)
                signing_up_user=MainUser(signup_form.cleaned_data['username'])
                # signup_user=MainUser(signup.cleaned_data['username'])

                info=signing_up_user.get_signup_info(request.POST,signup_form.cleaned_data)
                password=info['password']
                password2=info['password2']

                if signing_up_user.check_passwords(password,password2):
                    if signing_up_user.user_exists(info['username'],password):
                        message="Username already exists"
                    else:
                        context={"message":"Registered"}

                        signing_up_user.sign_up(info)
                        return HttpResponseRedirect('login')
                else:
                    message="Sorry, unmatched passwords"
            else:
                message="Some details wrongly entered... Sorry,can't register"

        else:
            
            signup_form=Signupform()

        context={'username':signup_form['username'],'telegram_username':signup_form['telegram_username']
                ,'password':signup_form['password'],'phone_number':signup_form['phone_number'],
                'maincontrollerID':signup_form['maincontrollerID'],'message':message}

        return  render(request,"sign_up.html",context)
    except Exception as expt:
        print(f"{expt} occured at signup in views")
        return HttpResponseRedirect('login')
        


# sign up added user view
def sigupadded(request):
    try:
        signupadded_form=Signupaddedform()
        message=''
        if request.session['is_logged_in']:
            if request.method == 'POST':

                signupadded_form=Signupaddedform(request.POST)
                if signupadded_form.is_valid():

                    signing_up_subuser=SubUser(signupadded_form['username'])
                    signup_info= signing_up_subuser.signupadded_info(request.POST,fromform=signupadded_form.cleaned_data)
                    password=signup_info['password']
                    password2=signup_info['password2']

                    validate=signing_up_subuser.check_passwords(password,password2)
                    if validate:
                        if signing_up_subuser.user_exists(signup_info['username'],password):
                            message="Username already exists"
                            print(message)
                        else:
                            message='Registered'
                            signing_up_subuser.sign_up_added(signup_info)
                            print(message)
                            return index(request)
                    
                    else:
                        message="Sorry, matching passswords"
                else:
                    pass
                    
            else:
                signupadded_form=Signupaddedform()
                # return render(request,login)
        else:
            pass
        
        context={'username':signupadded_form['username'],'telegram_username':signupadded_form['telegram_username']
        ,'password':signupadded_form['password'],'phone_number':signupadded_form['phone_number'],
        'verification_id':signupadded_form['verification_id'],"maincontroller":signupadded_form['maincontrollerID'],message:'message'}
        
        return render(request,"sign_up_added.html",context)

    except Exception as e:
        print(f"{e} occured at signupadded_formaddded in views")
        return HttpResponseRedirect('login')
        


#The main user adding another user
def add_user(request):
    try:
        add_user_form=addduserform()
        message=''
        verification_key_text=''
        if request.session['is_logged_in']:
            if request.method=='POST':
                add_user_form=addduserform(request.POST)
                if add_user_form.is_valid():
                    username=add_user_form.cleaned_data['added_username']
                    username2=add_user_form.cleaned_data['added_username2']
                    # creating user instances
                    adding_user_main=MainUser(username)
                    adding_user_sub=SubUser(username)

                    if (username == username2)  and not(adding_user_sub.user_exists_added(username)):
                        
                        get_key=generate_verification_id(username)
                        verification_key_text="{} Verification ID is: {}".format(username.upper(),get_key)
                        adding_user_main.add_new_user(username,request.session['id'],get_key)
                        message='Added succefully.'
                    else:
                        message='user already exist or unmatching names entered or please log in'
            
            else:
                add_user_form=addduserform()
        else:
            return HttpResponseRedirect('login')

        context={'message':message,'username':add_user_form['added_username'],'username2':add_user_form['added_username2'],'verify_message':verification_key_text}
        return render(request,"add_user.html",context)
    
    except Exception as expt:
        print(expt,"occured at add_user in views")
        return HttpResponseRedirect('login')
        




def device_operations(request):
    try:
     
        deviceform=adddeviceform()
        device_obj=Devices(request.session['id'])#creating device object
        devices_db=device_obj.get_connected_devices(request.session['id'])
        
        devices=set({})
        device_name=''
        status=''
        devices_dict=(string_no_space_dict(devices))

        schedule_device=""
        add_schedule=False
            
        # print(devices_dict,devices,devices_db)
        new_status={}
        for i in devices_db.items():
            new_status[i[0].replace(" ","_")]=i[1]

        if len(devices_db)!=0:
            for i in devices_db.keys():
                devices.add(i)
        else:
            pass

        add_device=request.GET.get('add_device')

        if add_device:#check if one wants to add devices
            deviceform=adddeviceform(request.GET)
            pin_number=deviceform['pin_number'].value()
            added_device_name=deviceform['device_name'].value()
            maincontrollerid= request.session['id']

            # device_name=added_device_name
            if added_device_name or pin_number:
                device_obj.save_device_connected(maincontrollerid,added_device_name,pin_number)

            # remove None type object
            devices.add(added_device_name)
            if None in devices:
                devices.remove(None)

            devices_dict=(string_no_space_dict(devices))
        

        elif request.GET.get('devices'):
            devices_dict=string_no_space_dict(devices)

        elif request.GET.get('add_schedule'):
            schedule_device=request.GET.get('add_schedule')
            schedule_device=schedule_device.replace("_"," ")
            add_schedule=True

        else:
            get_device_status=request.GET
            for name,status in get_device_status.items():
                # changing on->True and off->False
                if status=="on":
                    status=True
                else:
                    status=False
                # editing device details
                devices_db[name.replace('_'," ")]=status
                status_formated=("On" if status else "Off")
                print(status_formated)
                new_status[name]= status_formated
                device_name=name

            devices_dict=string_no_space_dict(devices)

            #updating device status
            print(new_status.items())
            device_obj.update_device_status(request.session['id'],device_name.replace("_"," "),status)
    
        
        context={'device_name_form':deviceform['device_name'],'pin_number':deviceform['pin_number'],'isdevice':add_device,"mydevices":devices_dict.items(),"status":new_status.items(), "is_schedule":add_schedule,"device_scheduled":schedule_device}
        
        # return render(request,"?")
        return render(request,"device_operations.html",context)

    except Exception as expt:
        print(expt,"occured at device_operations views")
        return HttpResponseRedirect("login")


#home page view
def home(request):
    try:
        if request.session['is_logged_in']:
            if request.GET =={}:
                try:
                    context={"level":request.session['level'] }
                    return render(request,"home.html",context)
                except Exception as error:
                    context={"level":False}
                    return render(request,"home.html",context)


            elif request.GET.get('add_user'):
                return add_user(request)

            elif request.GET.get('devices'):
                return device_operations(request)

            elif request.GET.get('add_device'):
                return device_operations(request)
            # elif request.GET.get("add_sc")
            else:
                return device_operations(request)
        else:
            pass 
    except Exception as e:
        print(f"{e} occured at home in views")
        return HttpResponseRedirect('login')
        


# logout view
def logout(request):
    try:
        try:
            del request.session['id']
            del request.session['username']
            del request.session['level']

            request.session['islogged']=False
            return render(request,"logout.html")
        except Exception as error: 
            print(f"{error} occured in logout in views") 
            return render(request,"logout.html")
   
            
    except Exception as error:
        print(error,"at logout view")
        return HttpResponseRedirect('logot')
       




# schedule view
def schedule(request):
    try:
        if request.session['is_logged_in']:
            return render(request,"schedule.html")
    except Exception as error:
        print(f"{error} occured at scedule in views")


def edit_user_details(request):
    try:
        if request.session['is_logged_in']:
            new_details=request.POST #details submitted by user
            username=request.session["username"]
            loged_user=User(username)
            details=loged_user.get_user_details(username)
            message=""

            available_phone=details.Phone_number
            available_telegram_username=details.Telegram_username
            available_password=details.Password
            if request.POST=={}:
                pass
            # if is only editing username,phone number and telegram username
            elif request.POST['edit']=='Edit':
                new_username=new_details['username']
                new_phone_number=new_details['phone_number']
                new_telegram_username=new_details['telegram_name']
                edited=loged_user(Name=new_username,Telegram_username=new_telegram_username,Phone_number=new_phone_number)
                print(edited)
                
                message="Details Changed"
            # if is  editing username,phone number and telegram username and password
            else:
                if new_details['old_password']==available_password:
                    password_1=new_details['new_password_1']
                    password_2=new_details['new_password_2']
                    new_username=new_details['username']
                    new_phone_number=new_details['phone_number']
                    new_telegram_username=new_details['telegram_name']

                    is_same=loged_user.check_passwords(password_1,password_2)
                    edited=loged_user(Name=new_username,Telegram_username=new_telegram_username,Phone_number=new_phone_number)
                    print(edited)
                    message="Password changed" if is_same else "Unmatched Password re-entered"

                else:
                    message="Sorry,.. Wrong old password"


            context={"Phone":available_phone,"Telegram":available_telegram_username,"message":message}
            return render(request,"edit_user_details.html",context)

    except Exception as error:
        print(f"{error} occured at edit_user_details in views")
        return HttpResponseRedirect("login")
        

# view to edit device details
def edit_devices_details(request):
    try:
        if request.session['is_logged_in']:
            device=Devices("none")
            maincontrollerid=request.session['id']
            connected=device.get_connected_devices_details(maincontrollerid)
            print(connected.items())
            context={"connected_devices":connected.items()}
        return render(request,"edit_devices_details.html",context)
    except Exception as error:
        print(f"{error} occured at edit_device_details in views")
        return HttpResponseRedirect('login')