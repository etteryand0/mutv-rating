# # # # # # # # # #
# ° mutv Rating ° #
# =============== #
# Это ТелеБот со- #
# ставляющий рей- #
# тинг по количе- #
# ству набранных  #
# баллов детьми,  #
# поступающих в   #
#    МАШ РС(Я)    #
# =============== #
# Всё авторство   #
# принадлежит     # \ \ # github.com/etteryand0/ #
# Ознакомьтесь с лицен-  #
# зией перед использова- #
# нием, редактированием  #
# или распространением   #
# mutv Rating            #
# # # # # # # # # # # # #

import time # чтобы спать
import telepot # для работы с Telegram API
from telepot.loop import MessageLoop
import sqlite3 # работать с бд, чтобы банить id
import datetime # чтобы банить id по времени
from parser import Parser # для парсинга рейтинга

# Код, чтобы создать и очистить бд ban.db
bd_conn = sqlite3.connect('ban.db')
bd_cursor = bd_conn.cursor()

# Создать таблицу ban
bd_cursor.execute('TRUNCATE TABLE ban')
bd_cursor.execute('CREATE TABLE ban (name text, user text, full text)')

print('База данных подключена')
Parser = Parser('8','mutv').parse_data(False)
rating8 = Parser.rating
Parser = Parser('7','bgzf').parse_data(False)
rating7 = Parser.rating

for list_ in [rating8,rating7]:
  for rate in list_:
    time = datetime.datetime.now()
    delta = datetime.timedelta(minutes=10)
    bd_cursor.execute('INSERT INTO ban VALUES ("{1}","{0}","{0}")'.format(time - delta,rate[1][1]))
  
print('База данных настроена. Включаю бота')

# функция для анализа сообщения
def handle_bot(msg):
  from parser import Parser
  help = '*[?]* Чтобы составить рейтинг, нам нужны следующие данные:\n  1) _Класс_\n  2) _Имя пользователя_\nПример использования: Отправить сообщение:\n  _8 mutv_'
  no_user = '*[-]* Я не смог найти такого ученика'
  content_type, chat_type, chat_id = telepot.glance(msg)

  # TODO функция бана
  with open('ban.db','r') as f:
    ban = [i.strip() for i in f.readlines()]

  try:
    args = msg['text'].split()
  except KeyError:
    args = ['']

  if content_type == 'text':
    if args[0] == '7' or args[0] == '8':
      try:
        if len(args[1]) == 4:
          Parser = Parser(args[0],args[1].lower())

          if Parser.parse_data(False):
            bot.sendMessage(chat_id, Parser.output)
            time.sleep(1)
            bot.sendMessage(chat_id, 'Спасибо, что используете меня! Мой отец - etteryand0 (mutv в МАШ)\n\nПодробнее о mutv Rating вы можете узнать по этой ссылке: https://github.com/etteryand0/mutv-rating')
        elif args[1] == 'all':
          try:
            if len(args[2]) == 4:
              Parser = Parser(args[0],args[2].lower())
                
              if Parser.parse_data(True):
                for rating in Parser.output:
                  output = ''
                  for pupil in rating:
                    output += pupil+'\n'
                  bot.sendMessage(chat_id, output)
                  time.sleep(1)
                
                bot.sendMessage(chat_id, 'Спасибо, что используете меня! Мой отец - etteryand0 (mutv в МАШ)\n\nПодробнее о mutv Rating вы можете узнать по этой ссылке: https://github.com/etteryand0/mutv-rating')
              else:
                bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
            else:
              bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
          except IndexError:
            bot.sendMessage(chat_id, help, parse_mode='Markdown')
        else:
          bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
      #else:
        #bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
      except IndexError:
        bot.sendMessage(chat_id, help, parse_mode='Markdown')

    elif args[0] == '10':
      bot.sendMessage(chat_id, '[-] Поддерживаются только 7 и 8 классы')
    else:
      bot.sendMessage(chat_id, help, parse_mode='Markdown')

# открыть файл с Telegram Bot Api и создать связь с ботом.
with open('bot_api.txt','r') as f:
  API = f.readline().strip()
  bot = telepot.Bot(API)

MessageLoop(bot,handle_bot).run_as_thread() # Запустить слушатель

while True:
  time.sleep(2)
