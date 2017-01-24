# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import pprint
from urllib.parse import parse_qs
import webbrowser
import pickle
from datetime import datetime, timedelta
import vk
import time
import vk_requests

# id of vk.com application
APP_ID = 5745809
# file, where auth data is saved
AUTH_FILE = '.auth_data'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'
#vk_requests
#api = vk_requests.create_api(app_id=123, login='User', password='Password')
#api = vk_requests.create_api(app_id=123, login='User', password='Password', phone_number='+79111234567')

def send_message(api, user_id, message, **kwargs):
    data_dict = {
        'user_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.messages.send(**data_dict)

def main():
    #открытие текста сообщения, read-only
    msg = open('text.txt', 'r')
    user_text = msg.read()

    #чтение логинов-паролей ботов из файла
    log = []
    psw = []
    f = open('bots.txt', 'r')
    bots = f.readlines()
    k=0
    l=0
    p=0
    #занесение л/п в списки
    while k <= 13:
        log.append(bots[k])
        k=k+1
        psw.append(bots[k])
        k=k+1

    #рассылка#

    #обнуление номера строки получателей
    list_num = 0
    #обнуление успешных отправок
    done=0
    #обнуление номера бот-аккаунта
    t=0
    #первоначальная авторизация
    api = vk_requests.create_api(app_id=APP_ID, login=log[t], password=psw[t][0:-1], phone_number=log[t], scope=['offline', 'messages'])
    #открытие списка получателей из файла построчно, строка -> элемент списка
    with open("currlist.txt") as file:
        users = [row.strip() for row in file]
    #для каждого элемента списка
    for user_id in users:
        if done==2:
            t=t+1
            api = vk_requests.create_api(app_id=APP_ID, login=log[t], password=psw[t][0:-1], phone_number=log[t], scope=['offline', 'messages'])
            done=0
        list_num = list_num + 1
        print("User num - ", list_num, ' Link - vk.com/id', user_id, sep='')
        #обработка ошибок#
        #первоначальное действие
        #res = send_message(api, user_id=user_id, message=user_text)
        try:
            res = send_message(api, user_id=user_id, message=user_text)
        #если вываливается ошибка, то
        except Exception:
            print('Ошибка для ', list_num, user_id)
        #если удачно, то
        else:
            print('Удачно!')
            done=done+1
        #в любом случае, в конце делать
        finally:
            time.sleep(1)
main()
