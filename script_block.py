# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import pprint
from urllib.parse import parse_qs
import webbrowser
import pickle
from datetime import datetime, timedelta
import vk
import time

# id of vk.com application
APP_ID = 5745809
# file, where auth data is saved
AUTH_FILE = '.auth_data_block'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'

def get_saved_auth_params():
    access_token = None
    user_id = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            access_token = token
            user_id = uid
    except IOError:
        pass
    return access_token, user_id


def save_auth_params(access_token, expires_in, user_id):
    expires = datetime.now() + timedelta(seconds=int(expires_in))
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)
        pickle.dump(expires, output)
        pickle.dump(user_id, output)


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=wall,messages&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token".format(app_id=APP_ID))
    webbrowser.open_new_tab(auth_url)
    redirected_url = input("Paste here url you were redirected:\n")
    aup = parse_qs(redirected_url)
    aup['access_token'] = aup.pop(
        'https://oauth.vk.com/blank.html#access_token')
    save_auth_params(aup['access_token'][0], aup['expires_in'][0],
                     aup['user_id'][0])
    return aup['access_token'][0], aup['user_id'][0]

def send_message(api, user_id, message, **kwargs):
    data_dict = {
        'user_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.messages.send(**data_dict)

def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)


def main():
    #
    access_token, _ = get_saved_auth_params()
    if not access_token or not _:
        access_token, _ = get_auth_params()
    api = get_api(access_token)

    #открытие текста сообщения, read-only
    msg = open('text.txt', 'r')
    user_text = msg.read()

    #обнуление номера строки
    list_num = 0
    #открытие списка получателей из файла построчно, строка -> элемент списка
    with open("currlist.txt") as file:
        users = [row.strip() for row in file]
    #для каждого элемента списка
    for user_id in users:
        list_num = list_num + 1
        print("User num - ", list_num, ' Link - vk.com/', user_id, sep='')
        #обработка ошибок
        #первоначальное действие
        try:
            res = send_message(api, user_id=user_id, message=user_text)
        #если вываливается ошибка, то
        except Exception:
            print('Ошибка для ', list_num)
        #если удачно, то
        else:
            print('Удачно!')
        #в любом случае, в конце делать
        finally:
            time.sleep(3)


### НАЧАЛО ПРОГРАММЫ ###
main()
