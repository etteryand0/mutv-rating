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
# принадлежит \/  #
# \/ \/ \/ \/ \/ \/ \ \ \
# github.com/etteryand0/ #
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
db_cursor = db_conn.cursor()

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
          bot.sendMessage(chat_id, 'Пожалуйста подождите! Обрабатываю...')
          db_conn = sqlite3.connect('ban.db')
          db_curs = db_conn.cursor()

          try:
            db_curs.execute('SELECT once FROM ban WHERE id="%s"' % bot_api)
            fetch_time = db_curs.fetchone()[0]
          except:
            dtime = str(datetime.datetime.now() - datetime.timedelta(minutes = 10)).split('.')[0].split(' ')[1]
            db_curs.execute('INSERT INTO ban VALUES ("{0}","{1}","N")'.format(chat_id, dtime))
            db_conn.commit()
            fetch_time = dtime

          time_diff = (datetime.datetime.strptime(str(datetime.datetime.now()).split('.')[0].split(' ')[1], '%H:%M:%S') -  datetime.datetime.strptime(fetch_time, '%H:%M:%S') )

          if time_diff.seconds < 120: # не прошло 120 минут
            time.sleep(1)
            bot.sendMessage(chat_id, banned % str(120-time_diff.seconds), parse_mode='Markdown')
          else: # прошло 120 минут с бана. Парсим
            Parser = Parser(args[0],args[1].lower())
            if Parser.parse_data(False):
              bot.sendMessage(chat_id, Parser.output)
              time.sleep(1)
              bot.sendMessage(chat_id, 'Спасибо, что используете меня! Мой отец - etteryand0 (mutv в МАШ)\n\nПодробнее о mutv Rating вы можете узнать по этой ссылке: https://github.com/etteryand0/mutv-rating')
              dtime = str(datetime.datetime.now()).split('.')[0].split(' ')[1]
              db_curs.execute('UPDATE ban SET once="{0}" WHERE id="{1}"'.format(dtime,chat_id))
              db_conn.commit()
            else:
              bot.sendMessage(chat_id, no_user, parse_mode="Markdown")
          db_conn.close()
        elif args[1] == 'all':
          try:
            if len(args[2]) == 4:
              # Parser = Parser(args[0],args[2].lower())
              bot.sendMessage(chat_id, 'Пожалуйста, подождите! Обрабатываю...')
              db_conn = sqlite3.connect('ban.db')
              db_curs = db_conn.cursor()

              try:
                db_curs.execute('SELECT full FROM ban WHERE id="{0}"'.format(chat_id))
                fetch_status = db_curs.fetchone()[0]
              except:
                dtime = str(datetime.datetime.now() - datetime.timedelta(minutes = 10)).split('.')[0].split(' ')[1]
                db_curs.execute('INSERT INTO ban VALUES ("{0}","{1}","N")'.format(chat_id,dtime))
                db_conn.commit()
                fetch_status = 'N'
              
              if fetch_status == 'Y':
                  time.sleep(1)
                  bot.sendMessage(chat_id,"# Hey", parse_mode="Markdown")
              else:
                if Parser.parse_data(True):
                  for rating in Parser.output:
                    output = ''
                    for pupil in rating:
                      output += pupil+'\n'
                    bot.sendMessage(chat_id, output)
                    time.sleep(1)
                    bot.sendMessage(chat_id, 'Спасибо, что используете меня! Мой отец - etteryand0 (mutv в МАШ)\n\nПодробнее о mutv Rating вы можете узнать по этой ссылке: https://github.com/etteryand0/mutv-rating')
                    db.curs.execute('UPDATE ban SET full="Y" WHERE id="{0}"'.format(chat_id))
                    db.conn.commit()
                else:
                  bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
              db_conn.close()
            else:
              bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
          except IndexError:
            time.sleep(0.5)
            bot.sendMessage(chat_id, help, parse_mode='Markdown')
        else:
          time.sleep(0.7)
          bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
      except IndexError:
        time.sleep(1)
        bot.sendMessage(chat_id, help, parse_mode='Markdown')

    elif args[0] == '10':
      time.sleep(1)
      bot.sendMessage(chat_id, '[-] Поддерживаются только 7 и 8 классы')
    else:
      time.sleep(0.5)
      bot.sendMessage(chat_id, help, parse_mode='Markdown')

# открыть файл с Telegram Bot Api и создать связь с ботом.
with open('bot_api.txt','r') as f:
  API = f.readline().strip()
  bot = telepot.Bot(API)

MessageLoop(bot,handle_bot).run_as_thread() # Запустить слушатель

while True:
  time.sleep(2)
