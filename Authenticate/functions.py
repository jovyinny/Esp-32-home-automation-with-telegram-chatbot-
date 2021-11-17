import re,random,time
from Authenticate.models import Connected_devices, Maincontroller,Users


class User:
    def __init__(self,username):
        self.username=username

    def check_passwords(self,password,password2):
        if password==password2:
            return True
        else:
            return False

    def get_user_details(self,username):
        try:
            details=Users.objects.get(Name=username)
            return details
        except Exception as error:
            print(f"{error} occured at get_user_details")
    # password
    def get_user_password(self,username):
        try:
            user_details=Users.objects.get(Name=username).Password
            return user_details

        except Exception as error:
            print(f"{error} occured at get_user_password in functions.py")
            return False

    # get the user level (main or subuser) Main->True, subuser->False or not found->false
    def is_user_main_level(self,username):
        try:
            obj=Users.objects.get(Name=username)
            obj_level=obj.Level
            print(obj_level,"in get_user_level")
            if len(obj_level)==0:
                return False
            else:
                if obj_level=="Main":
                    return True
                else:
                    return False        
            # return obj_level

        except Exception as error:
            print(f"{error} occurred at get_user_level at functions.py")

    #check whether user is already registered
    def user_exists(self,username,password):
        try:
            name_db=Users.objects.get(Name=username,Password=password)
            return True
        except Exception as error:
            print(f"{error} occured at user_exists function")
            return False

    pass


class MainUser(User):
    # def __init__(self,username):
    #     self.username=username

    def check_mainuser(self,controller):
        try:
            obj=Users.objects.filter(MaincontrollerID__MaincontrollerID=controller).values()
            obj2=Maincontroller.objects.filter(MaincontrollerID=controller).values()
            # print(obj,'check',obj2)
            if len(obj) !=0:
                return False
            else:
                return True
        except Exception as error:
            print(f"{error} occured at check_mainuser function in functions.py")


    #get user sign up info from the submitted form
    def get_signup_info(self,fromhttp,fromform):
        try:
            username=fromform['username']
            phone_number=fromform['phone_number']
            maincontrollerID=fromform['maincontrollerID']
            password=fromform['password']
            password2=fromhttp['password2']
            telegram_username=fromform['telegram_username']

            info={'username':username,'phone_number':phone_number,'maincontrollerID':maincontrollerID,"telegram_username":telegram_username,'password':password,'password2':password2}
            return info

        except Exception as error:
            print(f"{error} occured at get_signup_info functions.py")

    
    #add user
    def add_new_user(self,name,maincontroller,verification):
        try:
            id=Maincontroller.objects.get(MaincontrollerID=maincontroller)
            new_user=Users(Name=name,MaincontrollerID=id, Verification_id=verification)
            new_user.save()

        except Exception as err:
            print(err,"occured at added_user in Authenticate/functioncs.py")

    

    # Signing up the main user
    def sign_up(self,userinfo):
        try:
            username=userinfo['username']
            phone_number=userinfo['phone_number']
            maincontrollerID=userinfo['maincontrollerID']
            password=userinfo['password']
            telegram_username=userinfo['telegram_username']
            if self.check_mainuser(maincontrollerID):
                level="Main"
                obj=Maincontroller.objects.filter(MaincontrollerID=maincontrollerID)
                maincontroller_obj=Maincontroller(obj.values()[0]['MaincontrollerID'])
                new_user=Users(Name=username,Telegram_username=telegram_username,Level=f"{level}",Password=password,Phone_number=phone_number,MaincontrollerID=maincontroller_obj)
                new_user.save()
            else:
                level="subuser"
                
            return True
        except Exception as error:
            print("{} occured at sign_up function in function.py".format(error))
            return False





class SubUser(User):
    
    #check whether the verification id is valid
    def check_verification(self,id):
        try:
            obj=Users.objects.get(Verification_id=id)
            if obj:
                return True,obj
            else:
                return False

        except Exception as err:
            print(err,"occured at check_verification in functions.py")



    def user_exists_added(self,username):
            name_db=Users.objects.filter(Name=username)
            try:
                # print(len(name_db))
                if len(name_db)==0:
                    return False
                else:
                    return True
            except Exception as error:
                print(f"{error} occured at user_exists_added at function.py")
                return True

    #get added user sign up info from the submitted form(from http response and djang form)
    def signupadded_info(self,fromhttp,fromform):
        try:
            password2=fromhttp['password2']
            username=fromform['username']
            phone_number=fromform['phone_number']
            verification_id=fromform['verification_id']
            password=fromform['password']
            maincontroller=fromform['maincontrollerID']
            telegram_username=fromform['telegram_username']
            # creating dictionary with obtained values
            info={'username':username,'telegram_username':telegram_username,'phone_number':phone_number,'verification_id':verification_id,"maincontroller":maincontroller,'password':password,'password2':password2}

            return info

        except Exception as error:
            print(f"{error} occurred at signupadded_info in functions.py")

    # signing up asdded user
    def sign_up_added(self,userinfo):
        try:
            # unpacking information
            phone_number=userinfo['phone_number']
            password=userinfo['password']
            telegram_username=userinfo['telegram_username']
            verification_id=userinfo['verification_id']
            print("inhrer")
            if self.check_verification(verification_id)[0]:
                new_user=self.check_verification(verification_id)[1]
                new_user.Telegram_username=telegram_username
                new_user.Phone_number=phone_number
                new_user.Password=password
                # saving changes 
                new_user.save()
            else:
                return False
            
        except Exception as err:
            print(f"{err} occured at sign_up_added function")


# devices class
class Devices:
    def __init__(self,name):
        self.name=name
        pass

    def get_maincontroller(self,username):
        try:
            obj=Users.objects.get(Name=username)
            obj_id=obj.MaincontrollerID.MaincontrollerID
            return obj_id
        except Exception as err:
            print(err,"occured at get_maincontroller functions.py")
            return False


    # get registered connected device to particular maincontroller
    def get_connected_devices(self,controllerid):
        mydevices={}
        try:
            device=Connected_devices.objects.filter(MaincontrollerID=controllerid).values()
            if device=={}:
                pass
            else:
                for i in device:
                    mydevices[i['Device_name']]=i['Current_status']
            return mydevices
        except Exception as err:
            print(err,"occured at get_connected_devices functions.py")
    

    def get_connected_devices_details(self,controllerid):
        mydevices={}
        try:
            device=Connected_devices.objects.filter(MaincontrollerID=controllerid).values()
            if device=={}:
                pass
            else:
                for i in device:
                    mydevices[i['Device_name']]=[i['Current_status'],i['Pin_number']]
            return mydevices
        except Exception as err:
            print(err,"occured at get_connected_devices functions.py")

    # find out if device already added
    def is_device_available(self,device_id,name):
        try:
            obj=Connected_devices.objects.filter(MaincontrollerID=device_id,Device_name=name)
            if obj:
                return True
            else:
                return False
        except Exception as excpt:
            print(f"{excpt} occured at is_device_available")

    # saving the added devices
    def save_device_connected(self,device_id,name,pin_numder):
        try:
            obj=self.is_device_available(device_id,name)
            if not (obj):
                new_device=Connected_devices(MaincontrollerID=device_id,Device_name=name,Pin_number=pin_numder,Current_status=False)
            new_device.save()
            print(new_device)
        except Exception as excpt:
            print(f"{excpt} occured at save_device_connected")

    # update the devices status after user input
    def update_device_status(self,device_id,name,new_status):
        try:
            obj=Connected_devices.objects.get(MaincontrollerID=device_id,Device_name=name)
            if obj:
                obj.Current_status=new_status
                obj.save()
            else:
                print(obj,'at update_device_status')
                pass
        except Exception as error:
            print(f"{error} occured at update_device_status")
    pass



#Return the maincontoller id


#returns the current time and date for creating unique verification ids
def get_current_time_info():
    now=time.gmtime()#getting current time
    year=now.tm_year#a year
    mon=now.tm_mon#a month
    day=now.tm_mday#a day
    hour=(now.tm_hour+3)#an hour
    min=now.tm_min# minute
    sec=now.tm_sec#seconds
    timestring="{}{}{}".format(day,mon,year)

    #the added key contains the added integer value of the current hour,min and secs
    time_dict={'timestring':timestring,
    'added':hour+min+sec}#dictionary with time string 

    return time_dict


# generating the verification id for added user by passing current time details na name
def generate_verification_id(name,timedict=get_current_time_info()):
    # creating an initial from sent names
    initial=name.split()[0][0].upper()

    key_highest_limit=timedict['added']
    generated_key=random.randint(0,key_highest_limit)
    keystring_time=timedict['timestring']
    
    verification_id="{}{}{}{}".format(initial,keystring_time,key_highest_limit,generated_key)
    return verification_id
    

# remove spaces from set of devices -> replace spaces with underscores
def string_no_space_dict(myset):
    new_dict={}
    for i in myset:
        if " " in i:
            new_dict[i]=i.replace(" ","_")
        else:
            new_dict[i]=i

    return (new_dict)