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
from parser import Parser # для парсинга рейтинга

# функция для анализа сообщения
def handle_bot(msg):
  from parser import Parser
  help = '*[?]* Чтобы составить рейтинг, нам нужны следующие данные:\n  1) _Класс_\n  2) _Имя пользователя_\nПример использования: Отправить сообщение:\n  _8 mutv_'
  no_user = '*[-]* Я не смог найти такого ученика'
  content_type, chat_type, chat_id = telepot.glance(msg)
  
  try:
    args = msg['text'].split()
  except KeyError:
    args = ['']
  
  if content_type == 'text':
    if args[0] == '7' or args[0] == '8':
      try:
        if len(args[1]) == 4:
          Parser = Parser(args[0],args[1])
          if Parser.parse_data():
            bot.sendMessage(chat_id, Parser.output)
          else:
            bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
        else:
          bot.sendMessage(chat_id, no_user, parse_mode='Markdown')
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
