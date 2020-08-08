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
db_conn = sqlite3.connect('ban.db')
db_cursor = bd_conn.cursor()

# Создать таблицу ban
try:
  db_cursor.execute('CREATE TABLE ban (id text, once text, full text)')
except:
  db_cursor.execute('DROP TABLE ban')
  db_cursor.execute('CREATE TABLE ban (id text, once text, full text)')


db_conn.commit()
db_conn.close()
  
print('База данных настроена. Включаю бота')

# функция для анализа сообщения
def handle_bot(msg):
  from parser import Parser
  import sqlite3

  help = '*[?]* Чтобы составить рейтинг, нам нужны следующие данные:\n  1) _Класс_\n  2) _Имя пользователя_\nПример использования: Отправить сообщение:\n  _8 mutv_'
  no_user = '*[-]* Я не смог найти такого ученика'
  content_type, chat_type, chat_id = telepot.glance(msg)
  banned = '*[-]* Вы пока что не можете использовать эту функцию. Действует ограничение.\n%s секунд осталось до разблокировки'

  try:
    args = msg['text'].split()
  except KeyError:
    args = ['']

  if content_type == 'text':
    if args[0] == '7' or args[0] == '8':
      try:
        if len(args[1]) == 4:
          # Parser = Parser(args[0],args[1].lower())
          db_conn = sqlite3.connect('ban.db')
          db_curs = db_conn.cursor()

          try:
            db_curs.execute('SELECT once FROM ban WHERE id=?',(args[1],))
          except:
              time = str(datetime.datetime.now() - datetime.timedelta(minutes = 10)).split('.')[0].split(' ')[1]
              db_curs.execute('INSERT INTO ban VALUES ("{0}","{1}","{1}")'.format(chat_id, time))
            db_curs.execute('SELECT once FROM ban WHERE id=?',(args[1],))
          
          time_diff = (datetime.datetime.strptime(str(datetime.datetime.now()).split('.')[0].split(' ')[0], '%H:%M:%S') -  datetime.datetime.strptime(db_curs.fetchone()[0], '%H:%M:%S') ).seconds 

          if time_diff < 120: # прошло 120 минут 
            bot.sendMessage(chat_id, banned % str(120-time_diff), parse_mod='Markdown')
          else:
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
