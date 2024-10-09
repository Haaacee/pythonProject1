import random
import telebot
from telebot import types
import os
from fuzzywuzzy import fuzz
import sqlite3
import datetime
from google.cloud import dialogflow
import numpy as np
from database import Database
from tkinter import Tk, BOTH, Label, Button
from tkinter.ttk import Frame, Button, Style
import sys
from parser import *

TOKEN = '6630659984:AAFUgMdDRh5KOBzhILSS758FlECjD-npfKk' #Токен telegram бота
bot = telebot.TeleBot(TOKEN) #Передаем токен в telebot
BotDB = Database('.venv/botdb') #Определение местонахождения базы данных

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="support-pykk-2f07c1ebc073.json" #Путь к json файлу приват-ключа
                                                                              # для работы с dialogflow
session_client = dialogflow.SessionsClient() #Сессия клиента dialogflow
project_id = 'support-pykk' #Айди проекта, берется с json файла
session_id = 'sessions' #Указывается любое значение
language_code = 'ru' #Язык русский
session = session_client.session_path(project_id, session_id) #Значения передаются в dialogflow
user = 1


def obrabotkaotveta(chatid, message): #Функция по обработке ответов для запроса к БД
    requestdbcheck = message.split(" ")
    if requestdbcheck[0] == "Расписание" and requestdbcheck[1] == "сегодня": #Обработка расписания
        dateparu = datetime.datetime.today()
        answernew = BotDB.get_student_paru(dateparu.strftime("%Y-%m-%d"))
        nomerotveta = 0
        for x in answernew:
            list_otvetov = list(answernew[nomerotveta])
            Answerto = ("Время: " + str(list_otvetov[0]) + "\n" + "Предмет: " + str(list_otvetov[1]) + "\n" +
                        "Преподаватель: " + str(list_otvetov[2]))
            bot.send_message(chatid, Answerto)
            nomerotveta =+ 1
    elif requestdbcheck[0] == "предмет": #Обработка ответа по ФИО преподавателя
        str(message)
        predmet = message[8:]
        answernew = BotDB.get_predmet(predmet)
        bot.send_message(chatid, answernew)

#######################################################################################################################
#Команда "Старт"
@bot.message_handler(commands=["start"])
def start(message):
    if (not BotDB.user_exists(message.from_user.id)):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Абитуриент')
        btn2 = types.KeyboardButton('Студент')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Привет, я виртуальный помощник универститета, выбери одно из двух, '
                                          'что бы я понимал, чем я могу тебе помочь',reply_markup=markup)
        types.ReplyKeyboardRemove()
        bot.register_next_step_handler(message, after_start)
    else:
        userunverid = BotDB.get_user_id(message.from_user.id)
        bot.send_message(message.chat.id,'Привет, рад твоему возвращению, чем могу помочь ?' + "\n" +
                         'Твой ID: ' + str(userunverid), reply_markup=types.ReplyKeyboardRemove())
#######################################################################################################################
#Добавление пользователя в БД

def after_student(message):
    if(not BotDB.user_exists(message.text)):
        BotDB.add_user(int(message.text), message.from_user.id)
#######################################################################################################################
#После выбора Банковское дело/Колледж
def afterbankdeloplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
    btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
    btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Банковское дело".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014962'
                                          '/000014962_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdeloplan)
    elif message.text == '3 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Банковское дело".'
                                          ' Срок обучения 3 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014964'
                                          '/000014964_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML' ,reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdeloplan)
    elif message.text == '2 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Банковское дело".'
                                          ' Срок обучения 2 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014969'
                                          '/000014969_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdeloplan)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Банковское дело".'
                                          ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014966'
                                          '/000014966_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdeloplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdeloplan)

def afterbankdelo(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
        btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
        btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdeloplan)
    elif message.text == 'Посмотреть количество мест':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Банковское дело".', reply_markup=markup)
        bot.send_message(message.chat.id,'<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=38.02.07-,'
                                         '%D0%91%D0%B0%D0%BD%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5%20%D0%B4%D0%'
                                         'B5%D0%BB%D0%BE,-20">Ссылка на таблицу</a>', parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdelo)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterbankdelo)
#######################################################################################################################
#После выбора Торговое дело/Колледж
def aftertorgdeloplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
    btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
    btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Торговое дело".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015340'
                                          '/000015340_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdeloplan)
    elif message.text == '3 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Торговое дело".'
                                          ' Срок обучения 3 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015343'
                                          '/000015343_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdeloplan)
    elif message.text == '2 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Торговое дело".'
                                          ' Срок обучения 2 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015344'
                                          '/000015344_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdeloplan)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Торговое дело".'
                                          ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015341'
                                          '/000015341_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdeloplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdeloplan)

def aftertorgdelo(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
        btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
        btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdeloplan)
    elif message.text == 'Посмотреть количество мест':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Торговое дело".', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=38.02.08-,'
                                          '%D0%A2%D0%BE%D1%80%D0%B3%D0%BE%D0%B2%D0%BE%D0%B5%20%D0%B4%D0%B5%D0%BB%D0%BE,'
                                          '-40">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdelo)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdelo)
#######################################################################################################################
#После выбора Реклама/Колледж
def afterreklamaplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
    btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
    btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Реклама".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014941'
                                          '/000014941_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterreklamaplan)
    elif message.text == '3 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Реклама".'
                                          ' Срок обучения 3 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014949'
                                          '/000014949_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklamaplan)
    elif message.text == '2 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Реклама".'
                                          ' Срок обучения 2 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014951'
                                          '/000014951_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklamaplan)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Реклама".'
                                          ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014946'
                                          '/000014946_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklamaplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklamaplan)

def afterreklama(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
        btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
        btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklamaplan)
    elif message.text == 'Посмотреть количество мест':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Реклама".', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=42.02.01-,'
                                          '%D0%A0%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%B0'
                                          ',-35">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterreklama)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklama)
#######################################################################################################################
#После выбора Логистика/Колледж
def afterlogistikaplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
    btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
    btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Операционная деятельность в логистике".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014933'
                                          '/000014933_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistikaplan)
    elif message.text == '3 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Операционная деятельность в логистике".'
                                          ' Срок обучения 3 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014935'
                                          '/000014935_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistikaplan)
    elif message.text == '2 года 4 мес (Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Операционная деятельность в логистике".'
                                          ' Срок обучения 2 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014936'
                                          '/000014936_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistikaplan)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Операционная деятельность в логистике".'
                                          ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014934'
                                          '/000014934_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistikaplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistikaplan)

def afterlogistika(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 4 мес (Заочная)')
        btn3 = types.KeyboardButton('2 года 4 мес (Заочная)')
        btn4 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistikaplan)
    elif message.text == 'Посмотреть количество мест':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Операционная деятельность в логистике".', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=38.02.03-,'
                                          '%D0%9E%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%'
                                          'D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0'
                                          '%B2%20%D0%BB%D0%BE%D0%B3%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B5,-45'
                                          ',-35">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistika)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistika)
#######################################################################################################################
#После выбора Финансы/
def afterfinansuplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn3 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Финансы".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014942'
                                          '/000014942_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansuplan)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Финансы".'
                                          ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014943'
                                          '/000014943_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansuplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansuplan)

def afterfinansu(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansuplan)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Финансы".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=38.02.06-,'
                                          '%D0%A4%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D1%8B,'
                                          '-30">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansu)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansu)
#######################################################################################################################
#После выбора Программиование/Колледж
def afterprogramirovanieplanvuborprogrammist(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 4 мес (Очно-Заочная)')
    btn3 = types.KeyboardButton('3 года 10 мес (Очная)')
    btn4 = types.KeyboardButton('4 года 4 мес (Очно-Заочная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Информационные системы и программирование".'
                                          ' и направления "Программист"' + '\n' +
                         'Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014957'
                                          '/000014957_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborprogrammist)
    elif message.text == '3 года 4 мес (Очно-Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Информационные системы и программирование".'
                                          ' и направления "Программист"' + '\n' +
                                          ' Срок обучения 3 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014959'
                                          '/000014959_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborprogrammist)
    elif message.text == '3 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Информационные системы и программирование".'
                                          ' и направления "Программист"' + '\n' +
                                          ' Срок обучения 3 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014953'
                                          '/000014953_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborprogrammist)
    elif message.text == '4 года 4 мес (Очно-Заочная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Информационные системы и программирование".'
                                          ' и направления "Программист"' + '\n' +
                                          ' Срок обучения 4 год 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014955'
                                          '/000014955_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborprogrammist)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborprogrammist)

def afterprogramirovanieplanvuborveb(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 4 мес (Очно-Заочная)')
    btn3 = types.KeyboardButton('3 года 10 мес (Очная)')
    btn4 = types.KeyboardButton('4 года 4 мес (Очно-Заочная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Информационные системы и программирование".'
                         ' и направления "Разработчик веб и мультимедийных приложений"' + '\n' +
                         'Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014958'
                                          '/000014958_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborveb)
    elif message.text == '3 года 4 мес (Очно-Заочная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Информационные системы и программирование".'
                         ' и направления "Разработчик веб и мультимедийных приложений"' + '\n' +
                         ' Срок обучения 3 года 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014973'
                                          '/000014973_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborveb)
    elif message.text == '3 года 10 мес (Очная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Информационные системы и программирование".'
                         ' и направления "Разработчик веб и мультимедийных приложений"' + '\n' +
                         ' Срок обучения 3 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014972'
                                          '/000014972_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborveb)
    elif message.text == '4 года 4 мес (Очно-Заочная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Информационные системы и программирование".'
                         ' и направления "Разработчик веб и мультимедийных приложений"' + '\n' +
                         ' Срок обучения 4 год 4 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014972'
                                          '/000014972_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborveb)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborveb)

def afterprogramirovanieplanvubor(message):
    if message.text == 'Программист':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 4 мес (Очно-Заочная)')
        btn3 = types.KeyboardButton('3 года 10 мес (Очная)')
        btn4 = types.KeyboardButton('4 года 4 мес (Очно-Заочная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborprogrammist)
    elif message.text == 'Разработчик веб и мультимедийных приложений':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 4 мес (Очно-Заочная)')
        btn3 = types.KeyboardButton('3 года 10 мес (Очная)')
        btn4 = types.KeyboardButton('4 года 4 мес (Очно-Заочная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        bot.register_next_step_handler(message, afterprogramirovanieplanvuborveb)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvubor)

def afterprogramirovanie(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Программист')
        btn2 = types.KeyboardButton('Разработчик веб и мультимедийных приложений')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Выбери направление', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanieplanvubor)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Информационные системы и программирование".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=5-,09.02.07,'
                                          '-%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1'
                                          '%8B%D0%B5%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%'
                                          'D0%B8">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanie)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanie)
#######################################################################################################################
#После выбора Дошкольное/Колледж
def aftershkola(message):
    if message.text == 'Получить план обучения':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Дошкольное образование".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014929'
                                          '/000014929_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftershkola)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Дошкольное образование".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text='
                                          '%D0%94%D0%BE%D1%88%D0%BA%D0%BE%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D0%BE%D0%B1%'
                                          'D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%'
                                          'B5">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftershkola)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, aftershkola)
#######################################################################################################################
#После выбора Юрист/Колледж
def afteruristplanvuborsud(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Юриспруденция".'
                         ' и направления "Юрист в сфере судебного администрирования"' + '\n' +
                         'Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015336'
                                          '/000015336_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvuborsud)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Юриспруденция".'
                         ' и направления "Юрист в сфере судебного администрирования"' + '\n' +
                         ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015374'
                                          '/000015374_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvuborsud)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvuborsud)

def afteruristplanvuborobes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn5 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Юриспруденция".'
                         ' и направления "Юрист в сфере социального обеспечения"' + '\n' +
                         'Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015338'
                                          '/000015338_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvuborobes)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id,
                         'Вот план обучения для специальности "Юриспруденция".'
                         ' и направления "Юрист в сфере социального обеспечения"' + '\n' +
                         ' Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015339'
                                          '/000015339_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvuborobes)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvuborobes)

def afteruristplanvubor(message):
    if message.text == 'Юрист в сфере социального обеспечения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.register_next_step_handler(message, afteruristplanvuborobes)
    elif message.text == 'Юрист в сфере судебного администрирования':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.register_next_step_handler(message, afteruristplanvuborsud)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvubor)

def afterurist(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Юрист в сфере социального обеспечения')
        btn2 = types.KeyboardButton('Юрист в сфере судебного администрирования')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Выбери направление', reply_markup=markup)
        bot.register_next_step_handler(message, afteruristplanvubor)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Юриспруденция".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=40.02.04-,'
                                          '%D0%AE%D1%80%D0%B8%D1%81%D0%BF%D1%80%D1%83%D0%B4%D0%B5%D0%BD%D1%86%D0%B8%D1%'
                                          '8F,-70">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftershkola)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterurist)
#######################################################################################################################
#После выбора ПК Системы/Колледж
def aftercomputerplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('3 года 10 мес (Очная)')
    btn3 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Компьютерные системы и комплексы".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015350'
                                          '/000015350_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputerplan)
    elif message.text == '3 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Компьютерные системы и комплексы".'
                                          ' Срок обучения 3 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015350'
                                          '/000015350_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputerplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputerplan)

def aftercomputer(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('3 года 10 мес (Очная)')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputerplan)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Компьютерные системы и комплексы".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=%D0%9A%D0%BE%'
                                          'D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D1%8B%D0%B5%20%D1%81%D0%B8'
                                          '%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%D0%B8%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0'
                                          '%B5%D0%BA%D1%81%D1%8B">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputer)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputer)
#######################################################################################################################
#После выбора Дизайн/Колледж
def afterdizaun(message):
    if message.text == 'Получить план обучения':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Дизайн (по отраслям)".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015476'
                                          '/000015476_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterdizaun)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Дизайн (по отраслям)".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=%D0%94%D0'
                                          '%B8%D0%B7%D0%B0%D0%B9%D0%BD%20(%D0%BF%D0%BE%20%D0%BE%D1%82%D1%80%D0%B0%D1%'
                                          '81%D0%BB%D1%8F%D0%BC)">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterdizaun)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterdizaun)
#######################################################################################################################
#После выбора Физ-ра/Колледж
def afterfizkultura(message):
    if message.text == 'Получить план обучения':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Физическая культура".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000015478'
                                          '/000015478_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterfizkultura)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Физическая культура".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=49.02.01-,%D0%'
                                          'A4%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BA%D1%83%D0%'
                                          'BB%D1%8C%D1%82%D1%83%D1%80%D0%B0,-5">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterfizkultura)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterfizkultura)
#######################################################################################################################
#После выбора ИБ/Колледж
def afterbezopasnost(message):
    if message.text == 'Получить план обучения':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Обеспечение информационной '
                                          'безопасности автоматизированных систем".'
                                          ' Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014916'
                                          '/000014916_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterbezopasnost)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Обеспечение информационной '
                                          'безопасности автоматизированных систем".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=%D0%9E%D0%B1%D0%'
                                          'B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B8%D0%BD%D1%84%D0%BE'
                                          '%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9%20%D0%B1%D0%B5%D0'
                                          '%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B0%D0%B2%D1%82'
                                          '%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B'
                                          'D%D1%8B%D1%85%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC">Ссылка на таблицу</a>',
                         parse_mode='HTML',reply_markup=markup)
        bot.register_next_step_handler(message, afterbezopasnost)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterbezopasnost)
#######################################################################################################################
#После выбора Бухгалтер/Колледж
def afterbuhgalterplan(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
    btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
    btn3 = types.KeyboardButton('Назад')
    markup.row(btn1, btn2)
    markup.row(btn3)
    if message.text == '2 года 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Экономика и бухгалтерский учет '
                                          '(по отраслям)". Срок обучения 2 года 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014921'
                                          '/000014921_000000000.pdf?1728233117">План обучения</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalterplan)
    elif message.text == '1 год 10 мес (Очная)':
        bot.send_message(message.chat.id, 'Вот план обучения для специальности "Экономика и бухгалтерский учет '
                                          '(по отраслям)". Срок обучения 1 год 10 мес', reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/upload/umm_files/UMM/000014922'
                                          '/000014922_000000000.pdf?1728233117">План обучения</a>',
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalterplan)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalterplan)

def afterbuhgalter(message):
    if message.text == 'Получить план обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('2 года 10 мес (Очная)')
        btn2 = types.KeyboardButton('1 год 10 мес (Очная)')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Какая форма и срок обучения интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalterplan)
    elif message.text == 'Посмотреть количество мест':
        bot.send_message(message.chat.id, 'Вот ссылка на таблицу с указанием количества приемных мест'
                                          ' для специальности "Экономика и бухгалтерский учет (по отраслям)".',
                         reply_markup=markup)
        bot.send_message(message.chat.id, '<a href="https://www.muiv.ru/abitur/spo/number/#:~:text=45-,38.02.01,'
                                          '-%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D0%B1%D1%'
                                          '83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%'
                                          'B9">Ссылка на таблицу</a>', parse_mode='HTML',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalter)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    else:
        bot.send_message(message.chat.id, 'Боюсь напортачить с ответом, лучше выбери '
                                          'что-нибудь из списка', reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalter)
#######################################################################################################################
#После выбора из списка Колледжа/Абитуриент        Перечисление направлений
def afterkollej(message):
    if message.text == 'Банковское дело':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Банковское дело 38.02.07')
        bot.send_message(message.chat.id,
        '<b>Квалификация:</b> Специалист банковского дела', parse_mode='HTML',reply_markup=markup)
        bot.send_message(message.chat.id,
                         '· Осуществление, учет и контроль банковских операций по привлечению и размещению '
                         'денежных средств;' + '\n' + '· оказание банковских услуг клиентам в организациях '
                                                      'кредитной системы.',reply_markup=markup)

        bot.register_next_step_handler(message, afterbankdelo)
    elif message.text == 'Торговое дело':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Торговое дело 38.02.08')
        bot.send_message(message.chat.id,'Специальность "Торговое дело" открывает двери в мир бизнеса и '
                                         'предпринимательства. Вы сможете освоить основы управления торговлей, '
                                         'научиться строить выгодные торговые отношения и успешно продвигать '
                                         'товары на рынке.', reply_markup=markup)
        bot.register_next_step_handler(message, aftertorgdelo)
    elif message.text == 'Реклама':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Реклама 42.02.01')
        bot.send_message(message.chat.id, 'Профессиональная деятельность включает:' + '\n' +
                                          '· Разработку рекламных продуктов;'  + '\n' +
                                          '· Рекламные кампании;'  + '\n' +
                                          '· Выставочную деятельность.', reply_markup=markup)
        bot.register_next_step_handler(message, afterreklama)
    elif message.text == 'Операционная деятельность в логистике':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Операционная деятельность в логистике 38.02.03')
        bot.send_message(message.chat.id, '<b>Квалификация:</b> операционный логист.', parse_mode='HTML', reply_markup=markup)
        bot.send_message(message.chat.id, 'Профессиональная деятельность включает:' + '\n' +
                                          '· Планирование и организация логистического процесса в организациях '
                                          '(в подразделениях) различных сфер деятельности;' + '\n' +
                                          '· Управление логистическими процессами в закупках, '
                                          'производстве и распределении;' + '\n' +
                                          '· Оптимизация ресурсов организации (подразделения), связанных с управлением '
                                          'материальными и нематериальными потоками;' + '\n' +
                                          '· Оценка эффективности работы логистических систем и контроль логистических '
                                          'операций.', reply_markup=markup)
        bot.register_next_step_handler(message, afterlogistika)
    elif message.text == 'Финансы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Финансы 38.02.06')
        bot.send_message(message.chat.id, '<b>Квалификация:</b> операционный логист.', parse_mode='HTML', reply_markup=markup)
        bot.send_message(message.chat.id, 'Финансисты могут применять свои умения и знания на производстве, в '
                                          'бизнесе, в финансовой сфере, в науке, в банке, в консалтинговой компании.')
        bot.send_message(message.chat.id, 'Профессиональная деятельность включает:' + '\n' +
                                          'Организация и осуществление деятельности финансовых, планово-экономических и '
                                          'налоговых служб организаций различных организационно-правовых форм, '
                                          'финансово-экономических служб органов государственной власти и '
                                          'местного самоуправления.', reply_markup=markup)
        bot.register_next_step_handler(message, afterfinansu)
    elif message.text == 'Информационные системы и программирование':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Информационные системы и программирование 09.02.07')
        bot.send_message(message.chat.id, 'Профессиональная деятельность включает:' + '\n' +
                                               '· Проектирование информационных систем;' + '\n' +
                                               '· Знание языков UML, SQL и PL/SQl в СУБД (My SQL, MS SQL и ORACLE);' + '\n' +
                                               '· Работа в CA Process Modeler и системе MS Project;' + '\n' +
                                               '· Программирование в «1С Предприятие»;' + '\n' +
                                               '· Разработка приложений в среде Visual Studio.', reply_markup=markup)
        bot.register_next_step_handler(message, afterprogramirovanie)
    elif message.text == 'Дошкольное образование':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Дошкольное образование 44.02.01')
        bot.send_message(message.chat.id, 'Профессиональная деятельность включает:' + '\n' +
                                               '· Организовывать различные виды деятельности и общение детей раннего и '
                                          'дошкольного возраста.' + '\n' +
                                               '· Проводить педагогический мониторинг процесса и результатов обучения и '
                                          'воспитания детей раннего и дошкольного возраста' + '\n' +
                                               '· Планировать и организовывать процесс воспитания детей раннего и '
                                          'дошкольного возраста.' + '\n' +
                                               '· Проводить занятия с детьми раннего возраста с учетом их возрастных, '
                                          'индивидуальных и психофизических особенностей.', reply_markup=markup)
        bot.register_next_step_handler(message, aftershkola)
    elif message.text == 'Юриспруденция':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Юриспруденция 40.02.04')
        bot.send_message(message.chat.id, 'Специальность "Юриспруденция" по-прежнему остается одной из наиболее'
                                          ' популярных среди абитуриентов.' + '\n' + '\n' +
                                          'Студенты, обучающиеся по этому направлению, погружаются в мир права, учатся '
                                          'анализировать и применять нормативные акты, защищать интересы клиентов, '
                                          'разрешать юридические проблемы.', reply_markup=markup)
        bot.send_message(message.chat.id, 'Обучение нацелено на развитие как профессиональных, так и личностных '
                                          'качеств, например, критического мышления, а также умения логически строить '
                                          'аргументацию, глубоко изучать нормы законодательства и '
                                          'применять их на практике.' + '\n' + '\n' +
                                          'Выпускники специальности "Юриспруденция" успешно работают в юридической сфере,'
                                          ' занимаются правовым консультированием, защитой интересов клиентов в суде, '
                                          'разрабатывать правовые акты.', reply_markup=markup)
        bot.send_message(message.chat.id, 'Обучаясь на специальности Юриспруденция в нашем колледже Вы получите '
                                          'самые необходимые знания и навыки для успешной карьеры в '
                                          'юридической сфере.', reply_markup=markup)
        bot.register_next_step_handler(message, afterurist)
    elif message.text == 'Компьютерные системы и комплексы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Компьютерные системы и комплексы 09.02.01')
        bot.send_message(message.chat.id, 'Поступив на специальность Вы освоите IT-технологии и научитесь '
                                          'практическими навыками в области проектирования, администрирования и '
                                          'сопровождения компьютерных систем; сможете внедрять '
                                          'инновационные решения.', reply_markup=markup)
        bot.register_next_step_handler(message, aftercomputer)
    elif message.text == 'Дизайн (по отраслям)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Дизайн (по отраслям) 54.02.01')
        bot.send_message(message.chat.id, 'Специальность «Дизайн» предоставляет возможность погрузиться в '
                                          'захватывающий и разнообразный мир творчества и визуальных коммуникаций. '
                                          'В процессе обучения студенты осваивают широкий спектр знаний и навыков, '
                                          'которые позволяют им создавать уникальные дизайн-проекты.', reply_markup=markup)
        bot.register_next_step_handler(message, afterdizaun)
    elif message.text == 'Физическая культура':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Физическая культура 49.02.01')
        bot.send_message(message.chat.id, 'Поступив на специальность, вы приобретете не только знания в области'
                                          ' физической культуры и спорта, но и профессиональные педагогические навыки, '
                                          'необходимые для успешной работы с учащимися различного возраста и '
                                          'уровня подготовки.', reply_markup=markup)
        bot.register_next_step_handler(message, afterfizkultura)
    elif message.text == 'Обеспечение информационной безопасности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Обеспечение информационной безопасности автоматизированных систем 10.02.05')
        bot.send_message(message.chat.id, '<b>Квалификация:</b> «Техник по защите информации».',
                         parse_mode='HTML', reply_markup=markup)
        bot.send_message(message.chat.id, 'Защита информации - ключевой аспект современного мира цифровых '
                                          'технологий. Высококвалифицированные специалисты по обеспечению информационной '
                                          'безопасности играют важную роль в защите конфиденциальности, целостности и'
                                          ' доступности данных в автоматизированных системах.', reply_markup=markup)
        bot.register_next_step_handler(message, afterbezopasnost)
    elif message.text == 'Экономика и бухгалтерский учет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить план обучения')
        btn2 = types.KeyboardButton('Посмотреть количество мест')
        btn3 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Экономика и бухгалтерский учет (по отраслям) 38.02.01')
        bot.send_message(message.chat.id, '<b>Квалификация:</b> Бухгалтер.',parse_mode='HTML', reply_markup=markup)
        bot.send_message(message.chat.id, 'Профессиональная деятельность включает:'
                                               '· Бухгалтерский учет: ведение и контроль за финансовым учетом на '
                                          'предприятиях различных форм собственности;'
                                               '· Аудит: проверка финансовой отчетности организаций на предмет '
                                          'соответствия стандартам бухгалтерского учета;'
                                               '· Консалтинг: предоставление консультационных услуг в области '
                                          'экономики и финансов;'
                                               '· Финансовый анализ: анализ финансовой отчетности для оценки '
                                          'финансового состояния компаний.', reply_markup=markup)
        bot.register_next_step_handler(message, afterbuhgalter)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Банковское дело')
        btn2 = types.KeyboardButton('Торговое дело')
        btn3 = types.KeyboardButton('Реклама')
        btn4 = types.KeyboardButton('Операционная деятельность в логистике')
        btn5 = types.KeyboardButton('Финансы')
        btn6 = types.KeyboardButton('Информационные системы и программирование')
        btn7 = types.KeyboardButton('Дошкольное образование')
        btn8 = types.KeyboardButton('Юриспруденция')
        btn9 = types.KeyboardButton('Компьютерные системы и комплексы')
        btn10 = types.KeyboardButton('Дизайн (по отраслям)')
        btn11 = types.KeyboardButton('Физическая культура')
        btn12 = types.KeyboardButton('Обеспечение информационной безопасности')
        btn13 = types.KeyboardButton('Экономика и бухгалтерский учет')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        markup.row(btn7, btn8)
        markup.row(btn9, btn10)
        markup.row(btn11, btn12)
        markup.row(btn13)
        bot.send_message(message.chat.id, 'Выбери из указанного ниже списка, какая специальность тебя интересует'
                         + '\n' + 'И я расскажу всё, что о ней знаю', reply_markup=markup)
#######################################################################################################################
#После выбора из списка Дни открытых дверей/Абитуриент
def afterdnei(message):
    bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Дни открытых дверей')
    btn2 = types.KeyboardButton('Отсрочка от армии студентам')
    btn3 = types.KeyboardButton('Колледж')
    btn4 = types.KeyboardButton('Бакалавриат')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
    bot.register_next_step_handler(message, after_abiturient)

def afterdniotdverei(message):
    if message.text == 'Подробная информация':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'На наших днях открытых дверей Вы сможете:' + '\n' +
                         '· Получить информацию по специальностям и направлениям подготовки бакалавриата и магистратуры;' + '\n' +
                         '· Ознакомиться с правилами приёма в МУИВ и перечнем вступительных испытаний;' + '\n' +
                         '· Проконсультироваться с сотрудниками приёмной комиссии;' + '\n' +
                         '· Узнать о студенческой жизни и практике студентов;' + '\n' +
                         '· Задать вопросы представителям ректората и институтов;')
        btn1 = types.KeyboardButton('Назад')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'На днях открытых дверей абитуриенты и их родители знакомятся с руководством МУИВ, директорами институтов,'
                         ' профессорами, узнают о специальностях и направлениях подготовки, условиях обучения, студенческой жизни, '
                         'практике студентов, перспективах выпускников университета.' + '\n' '\n'
                         'Обязательно приходите, получить ответы на все свои вопросы и сделайте правильный выбор!', reply_markup = markup)
        bot.register_next_step_handler(message, afterdnei)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Чем ещё могу помочь ?', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Выбери что ещё тебя интересует', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
#######################################################################################################################
#После выбора из списка Абитуриент
def after_abiturient(message):
    if message.text == 'Дни открытых дверей':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Рад, что вам интересен этот вопрос.' + "\n" + '<a href="https://w'
        'ww.muiv.ru/abitur/dod/#:~:text=%D0%94%D0%BB%D1%8F%20%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8'
        '%D0%B8%20%D0%BD%D0%B0,%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8E%20%D0%BF%D1%80%D0%'
        'B8%D1%91%D0%BC%D0%BD%D0%BE%D0%B9%20%D0%BA%D0%BE%D0%BC%D0%B8%D1%81%D1%81%D0%B8%D0%B8">Перейдите по ссылке</a>, '
                                                                        'что бы оставить заявку', parse_mode='HTML', reply_markup=markup)
        btn1 = types.KeyboardButton('Подробная информация')
        btn2 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Могу рассказать более детально', reply_markup=markup)
        bot.register_next_step_handler(message, afterdniotdverei)

    elif message.text == 'Отсрочка от армии студентам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'По всем представленным у нас специальностям и направлениям подготовки университет '
                                          'имеет государственную аккредитацию.Это позволяет нашим студентам пользоваться правом на '
                                          'отсрочку от призыва на военную службу в период обучения.' + '\n' + ' Такая возможность '
                                          'существует как для студентов колледжа ЧОУВО «МУ им. С.Ю. Витте», так и для тех, кто'
                                          ' получает высшее образование.', reply_markup=markup)
        btn1 = types.KeyboardButton('Назад')
        markup.row(btn1)
        bot.send_message(message.chat.id,'Для того, что бы воспользоваться правом на отсрочку, необходимо:',
                         reply_markup=markup)
        bot.send_message(message.chat.id, 'Шаг первый' + '\n' + 'Необходимо взять в университете справку по форме №2.',
                         reply_markup=markup)
        bot.send_message(message.chat.id, 'Шаг второй' + '\n' + 'Своевременно пройти медицинскую комиссию.',
                         reply_markup=markup)
        bot.send_message(message.chat.id, 'Шаг третий' + '\n' + 'Явиться на заседание призывной комиссии для того, чтобы '
                                                                'ознакомиться с решением о предоставлении отсрочки.',
                         reply_markup=markup)
        bot.send_message(message.chat.id,
                         '*Только для студентов очной формы обучения',
                         reply_markup=markup)
        bot.register_next_step_handler(message, afterdnei)
    elif message.text == 'Колледж':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Банковское дело')
        btn2 = types.KeyboardButton('Торговое дело')
        btn3 = types.KeyboardButton('Реклама')
        btn4 = types.KeyboardButton('Операционная деятельность в логистике')
        btn5 = types.KeyboardButton('Финансы')
        btn6 = types.KeyboardButton('Информационные системы и программирование')
        btn7 = types.KeyboardButton('Дошкольное образование')
        btn8 = types.KeyboardButton('Юриспруденция')
        btn9 = types.KeyboardButton('Компьютерные системы и комплексы')
        btn10 = types.KeyboardButton('Дизайн (по отраслям)')
        btn11 = types.KeyboardButton('Физическая культура')
        btn12 = types.KeyboardButton('Обеспечение информационной безопасности')
        btn13 = types.KeyboardButton('Экономика и бухгалтерский учет')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        markup.row(btn7, btn8)
        markup.row(btn9, btn10)
        markup.row(btn11, btn12)
        markup.row(btn13)
        bot.send_message(message.chat.id, 'Выбери, какая специальность тебя интересует'
                         + '\n' + 'А я расскажу всё, что о ней знаю', reply_markup=markup)
        bot.register_next_step_handler(message, afterkollej)
    elif message.text == 'Бакалавриат':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Поступление')
        btn2 = types.KeyboardButton('День открытых дверей')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Выбери что-нибудь', reply_markup=markup)

#######################################################################################################################
#После старта
def after_start(message):
    if message.text == 'Абитуриент' and user == 1:
        bot.send_message(message.chat.id, 'Здорово!', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Дни открытых дверей')
        btn2 = types.KeyboardButton('Отсрочка от армии студентам')
        btn3 = types.KeyboardButton('Колледж')
        btn4 = types.KeyboardButton('Бакалавриат')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, 'Могу подсказать информацию для поступления', reply_markup=markup)
        bot.register_next_step_handler(message, after_abiturient)
    elif message.text == 'Студент':
        bot.send_message(message.chat.id, 'Напиши свой ID из личного кабинета', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, after_student)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Абитуриент')
        btn2 = types.KeyboardButton('Студент')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Выбери одно из двух',reply_markup=markup)
        bot.register_next_step_handler(message, after_start)


def afteradmin(message):
    if message.text == 'Обновить расписание':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        raspisanieparser()
        bot.send_message(message.chat.id, 'Расписание обновлено', reply_markup=markup)
    elif message.text == 'Выйти':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Вышли', reply_markup = types.ReplyKeyboardRemove())
        # bot.register_next_step_handler(message, handle_text)

# Получение сообщений от клиента
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Запись ответа
    if message.text == '-sudo i --admin --pass=123123':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Обновить расписание')
        btn2 = types.KeyboardButton('Выйти')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Чем будем сегодня заниматься ?', reply_markup=markup)
        bot.register_next_step_handler(message, afteradmin)
    else:
        text_input = dialogflow.TextInput(  # Текст запроса
            text=message.text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)  # Ввод запроса
        response = session_client.detect_intent(  # Ответ бота
            session=session, query_input=query_input)
        if response.query_result.fulfillment_text:  # Если ответ имеется
            obrabotkaotveta(message.from_user.id, response.query_result.fulfillment_text)
        else:  # В обратном случае
            bot.send_message(message.from_user.id, "Я тебя не понимаю")  # Я тебя не понимаю


# class Example(Frame):
#     def __init__(self, parent):
#         Frame.__init__(self, parent)
#         self.parent = parent
#         self.initUI()
#
#     def initUI(self):
#         self.parent.title("Виртуальный ассистент")
#         self.style = Style()
#         self.style.theme_use("default")
#
#         self.pack(fill=BOTH, expand=1)
#
#         quitButton = Button(self, text="Закрыть окно", command=sys.exit)
#         quitButton.place(x=100, y=100)
#
#
# def main():
#     root = Tk()
#     root.geometry("250x150+300+300")
#     Example(root)
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()


# Запускаем бота
bot.polling(none_stop=True)
