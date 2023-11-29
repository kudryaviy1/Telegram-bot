import telebot
import time
import json
from datetime import datetime
import models


ru_bot_text = json.load(open("RU.json", encoding="utf-8"))


def split_list(arr, wanted_parts=1):
    """ Разбить список на подсписки """
    arrs = []
    while len(arr) > wanted_parts:
        pice = arr[:wanted_parts]
        arrs.append(pice)
        arr = arr[wanted_parts:]
    arrs.append(arr)
    return arrs


def language_check(user_id):
    """Подгружаем файл с текстами ответов бота"""
    return ru_bot_text


def create_inlineKeyboard(key, row=0):
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_list = []
    count = 0
    for i in key:
        key_list.append(telebot.types.InlineKeyboardButton(
            text=i, callback_data=key.get(i)))
        count += 1

        if count >= row:
            keyboard.add(*[i for i in key_list])
            key_list = []
            count = 0
        if list(key.keys())[-1] == i:
            keyboard.add(*[i for i in key_list])
    return keyboard


def log(func):
    """Декоратор для красивых логов в консоли"""
    def wrapper(*args, **kwargs):
        message = args[0]
        print("\n ---------")
        print(datetime.now())
        if str(type(message)) == "<class 'telebot.types.Message'>":
            print("From: %s %s. (id: %s)\nText: %s" % (message.from_user.first_name,
                                                       message.from_user.last_name, message.from_user.id, message.text))
        elif str(type(message)) == "<class 'telebot.types.CallbackQuery'>":
            print("From: %s %s. (id: %s)\ncallback: %s" % (message.from_user.first_name,
                                                           message.from_user.last_name, message.from_user.id, message.data))
        return_value = func(*args, **kwargs)
        return return_value
    return wrapper


def create_markup(key:list, row=0):
    """Создать репли клавиатуру из списка"""
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    if row == 0 or row == 1:
        if isinstance(key, str):
            user_markup.add(key)
        else:
            for i in key:
                user_markup.add(i)
    else:
        key_list = key
        for i in split_list(key_list, row):
            user_markup.add(*[telebot.types.KeyboardButton(name)
                              for name in i])
    return user_markup


def reply_markup_combiner(*keyboards):
    """Комбинирование репли клавиатур"""
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    answer = []
    for i in keyboards:
        for x in i.keyboard:
            answer.append(x)
    for i in answer:
        if list(i) == i:
            user_markup.add(
                *[telebot.types.KeyboardButton(name['text']) for name in i])
        else:
            user_markup.add(i['text'])
    return user_markup


def create_inlineKeyboard_url(key, row=0):
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_list = []
    count = 0
    for i in key:
        key_list.append(telebot.types.InlineKeyboardButton(
            text=i, url=key.get(i)))
        count += 1

        if count >= row:
            keyboard.add(*[i for i in key_list])
            key_list = []
            count = 0
        if list(key.keys())[-1] == i:
            keyboard.add(*[i for i in key_list])
    return keyboard