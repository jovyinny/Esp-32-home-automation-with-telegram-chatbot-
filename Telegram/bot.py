import json,requests,time
from functions_bot import check_sent_text,get_bot_url,help

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url=get_bot_url()
    url = url + "getUpdates?timeout=10"
    # help(url)
    if offset:
        url+="&offset={}".format(offset)
    js = get_json_from_url(url)

    return js


def get_last_update_id(updates):
    update_ids=[]
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
    return max(update_ids)


def get_last_chat_id_and_text_and_username(updates):
  
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    username = updates["result"][last_update]["message"]["chat"]["username"]
    return (text, chat_id,username)


def send_message(text, chat_id,username):
    try:
        url=get_bot_url()
        text=check_sent_text(text,username)
        print(text)

        url = url + "sendMessage?text={}&parse_mode=Markdown&chat_id={}".format((text), chat_id)

        get_url(url)
    except Exception as error:
        print(f"some {error} occured")


def reply_all(updates):
    for update in updates['result']:
        try:
            text=update['message']['text']
            chat_id=update['message']['chat']['id']
            username=update['message']['from']['username']
            # print(update['chat']['id'],"reply all")
            # help(chat_id)
            print("replying to {} sent by {}".format(text,username))

            send_message(text,chat_id,username)
        except Exception as e:
            print(e,"exception")



def main():
    last_update_id=None

    while True:
        updates=get_updates(last_update_id)
        # print(updates)
        try:
            if len(updates['result']) >0:
                last_update_id=get_last_update_id(updates)+1
                reply_all(updates)
            else:
                return False

            time.sleep(0.5)
        except Exception as e:
            print(e," not found")


if __name__ == '__main__':
    main()