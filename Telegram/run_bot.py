import schedule,time
from functions_bot import connect
from bot import main

def runbot_at_given_time():
    if connect():
        print("running")
        main()

schedule.every(10).to(15).seconds.do(runbot_at_given_time)


while True:
    schedule.run_pending()
    time.sleep(1)