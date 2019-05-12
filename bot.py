#!./env1/bin/python3.5
# -*- coding: utf-8 -*-

import vk_api
from time import sleep
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import ast
from last import get_last
import requests
from db import *
from config import *
import random


vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

upload = vk_api.VkUpload(vk_session)

users_in_archive = []

def update_DB_list():
    ## IDEA: ИСПРАВИТЬ ТУТ
    data = get_last(count=0)
    k = 1
    text = ''
    messages = []
    for i in data:
        game = getGameData(i)
        if k <= 60:
            text += 'id: ' + str(i) + ' Дата: ' + game.get('date') + '\n' + game.get('teamName1') + ' — ' + game.get('teamName2') + '\n\n'
            k += 1
        else:
            messages.append(text)
            text = ''
            k = 1
    if text != '':
       messages.append(text)
    return messages


def send_game(user_id, game_id):
    write_msg(user_id, s='Пожалуйста, подождите...')

    data = getGameData(game_id)

    gamePNG = data.get('gamePNG')
    write_msg(user_id, attachment=gamePNG)

    video = data.get('video_attachment')
    if video != '':
        write_msg(user_id, attachment=video)

    photos = data.get('photos_url')
    if photos != []:
        write_msg(user_id, attachment=','.join(photos))



def show10db(user_id, count):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Меню', color=VkKeyboardColor.PRIMARY, payload= {"button": "menu", 'user_id': user_id})
    keyboard.add_button('Показать список архива', color=VkKeyboardColor.DEFAULT, payload= {"button": "DBlist", 'user_id': user_id})
    keyboard.add_button('Показать по 10', color=VkKeyboardColor.DEFAULT, payload= {"button": "DBlist_10", 'count': count + 10 , 'user_id': user_id})

    message = ''
    data = get_last(count=0)[::-1][count-10:count]

    text = ''

    for i in data:
        game = getGameData(i)
        text += 'id: ' + str(i) + ' Дата: ' + game.get('date') + '\n' + game.get('teamName1') + ' — ' + game.get('teamName2') + '\n\n'
    if text != '':
        write_msg(user_id, s=text, keyboard=keyboard)
    else:
        write_msg(user_id, s='Это все записи в базе данных', keyboard=keyboard)

def menu(user_id):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Недавние игры', color=VkKeyboardColor.DEFAULT, payload= {"button": "last", "user_id": user_id})
    # keyboard.add_button('Меню', color=VkKeyboardColor.PRIMARY, payload= {"button": "menu", 'user_id': user_id})
    keyboard.add_button('Архив игр', color=VkKeyboardColor.DEFAULT, payload= {"button": "archive", "user_id": user_id})
    keyboard.add_button('Будущие матчи', color=VkKeyboardColor.DEFAULT, payload= {"button": "coming", 'user_id': user_id})
    keyboard.add_line()
    keyboard.add_button('Посетить сайт', color=VkKeyboardColor.DEFAULT, payload= {"button": "site", "user_id": user_id})
    keyboard.add_button('Автор', color=VkKeyboardColor.DEFAULT, payload= {"button": "author", "user_id": user_id})
    return keyboard

def sendArchiveList(user_id):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Меню', color=VkKeyboardColor.PRIMARY, payload= {"button": "menu", 'user_id': user_id})
    keyboard.add_button('Показать список архива', color=VkKeyboardColor.DEFAULT, payload= {"button": "DBlist", 'user_id': user_id})
    keyboard.add_button('Показать по 10', color=VkKeyboardColor.DEFAULT, payload= {"button": "DBlist_10", 'count': 10 , 'user_id': user_id})

    messages = update_DB_list()
    #write_msg(user_id, s= 'Это список всех игр, находящихся в данный момент в архиве, для получения всей информации об игре, введите её ID (Пример: 324)', keyboard=keyboard)
    for message in messages:
        write_msg(user_id, s=message, keyboard=keyboard)
    write_msg(user_id, s= 'Это список всех игр, находящихся в данный момент в архиве, для получения всей информации о конкретной игре, просто напишите её ID', keyboard=keyboard)

def archive(user_id, text= None):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Меню', color=VkKeyboardColor.PRIMARY, payload= {"button": "menu", 'user_id': user_id})
    keyboard.add_button('Показать список архива', color=VkKeyboardColor.DEFAULT, payload= {"button": "DBlist", 'user_id': user_id})
    keyboard.add_button('Показать по 10', color=VkKeyboardColor.DEFAULT, payload= {"button": "DBlist_10", 'count': 10 , 'user_id': user_id})

    if user_id not in users_in_archive:
        users_in_archive.append(user_id)

    if text == None:
        write_msg(user_id, s='Напишите ID матча или нажмите "Показать список архива", чтобы получить все ID в архиве', keyboard=keyboard)
    elif text in getAllIds():
        send_game(user_id, text)
    else:
        write_msg(user_id, s='Матча с таким ID нет')



def last(user_id):
    last = get_last()
    AllgamePNG = []
    videos = []
    for id in last:
        data = getGameData(id)
        gamePNG = data.get('gamePNG')
        video = data.get('video_attachment')
        if video != None:
            videos.append(video)
        AllgamePNG.append(gamePNG)
    write_msg(user_id, attachment=','.join(AllgamePNG))
    write_msg(user_id, attachment=','.join(videos))



def coming(user_id):
    data = getAllIds(coming=True)
    message = ''
    k = 1
    for i in data:
        game = getGameData(-i)
        message += str(k) + '. ' + game.get('teamName1') + ' — ' + game.get('teamName2') + '\n' + game.get('date') + '\n' + game.get('place') + '\n\n'
        k += 1

    # IDEA: Сделать графическую тему для этого
    write_msg(user_id, s= message)



def write_msg(user_id, s=None, keyboard=None, attachment=None):
    try:
        if s != None and keyboard != None:
           vk.messages.send(user_id= user_id, message= s, keyboard=keyboard.get_keyboard(), random_id = random.randint(-100000,100000))
        elif s != None:
           vk.messages.send(user_id= user_id, message= s, random_id = random.randint(-100000,100000))
        elif attachment != None:
           vk.messages.send(user_id= user_id, attachment=attachment, random_id = random.randint(-100000,100000))
    except:
        print('flood control error')

# обработчик событий, запускает функцию answer, когда боту поступает сообщение, передаёт функции ID пользователя и текст сообщения
longpoll = VkBotLongPoll(vk_session, group_id)

#Try
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        try:
            payload = ast.literal_eval(event.obj.payload)
            print(payload)
            button_clicked = payload.get('button')
        except:
            button_clicked = None

        user_id = event.obj.from_id
        text = event.obj.text
        print(text + '  ' + str(user_id))

        try:
            text = int(text)

            if (user_id in users_in_archive):
                archive(user_id, text)
        except:
            pass
            # IDEA: Сделать оброботчик неверных сообщений



        if (button_clicked == 'menu') or (str(text).lower() == 'начать'):
            keyboard1 = menu(user_id)
            write_msg(user_id, keyboard= keyboard1, s='Главное меню')
            if user_id in users_in_archive:
                users_in_archive.remove(user_id)

        if button_clicked == 'archive':
            archive(user_id, text=None)

        if button_clicked == 'DBlist_10':
            show10db(user_id, count=payload['count'])

        if button_clicked == 'last':
            last(user_id)

        if button_clicked == 'author':
            keyboard1 = menu(user_id)
            write_msg(user_id, keyboard= keyboard1, s='Автор данного бота [val_kd|Валентин Казанцев]')

        if button_clicked == 'coming':
            coming(user_id)


        if button_clicked == 'DBlist':
            sendArchiveList(user_id)

        if button_clicked == 'site':
            keyboard1 = menu(user_id)
            write_msg(user_id, keyboard= keyboard1, s='Сайт Орского Хоккейного клуба http://www.orsk-hockey.ru/')
