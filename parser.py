# # # # # # # # # # # # #
# °       parser      ° #
# ===================== #
# Этот файл - библиоте- #
# ка для mutv Rating.   #
# Отвечает за работу с  #
# данными рейтинга уче- #
# ников, поступающих в  #
#          МАШ          #
# =============== # / / /
# Всё авторство   #
# принадлежит     # \ \ 
# github.com/etteryand0/ #
#                        #
# Ознакомьтесь с лицен-  #
# зией перед использова- #
# нием, редактированием  #
# или распространением   #
# mutv Rating            #
# # # # # # # # # # # # #


from bs4 import BeautifulSoup # for parsing
import requests # for GET request

# класс Parser для работы с html и данными
class Parser():
  def __init__(self,classroom, username):
    # функция инициализации. Требует от пользователя класс, в который поступает и его имя пользователя в МАШ
    # Генерирует ссылку и вызывает функцию для парсинга полученной html страницы
    self.rating = [] # глобальный массив для хранения рейтинга
    self.username = username
    self.near_rating = []
    self.output = ''
    link = 'http://arctic-school.com/exam7-8-results/exam-class%s/' % classroom # шаблон ссылки для парсинга
    self.parse_html(link)
  
  
  def prettify_output(self):
    # функция для оформления вывода
    # необходим для юзерфрендли статуса
    if self.near_rating[0][0] != 1:
      self.output += '..\n'
    for pupil in self.near_rating:
      id = str(pupil[0])
      id = str(int(id)+1)
      if pupil[1][1] == self.username:
        line = '{0}. {1} - {2} баллов < Вы здесь\n'.format(id,pupil[1][1],pupil[1][0])
      else:
        line = '{0}. {1} - {2} баллов\n'.format(id,pupil[1][1],pupil[1][0])
      self.output += line
    self.output += '..'
    print('%s served' % self.username)
  
  
  def parse_data(self):
    # функция сортировки данных. Сортирует глобальный массив результатов по убыванию баллов.
    # находит данное имя пользователя, сохраняет его и 10 самых ближних по баллу учеников
    self.rating = sorted(self.rating) # сортировка начиная с 0
    self.rating = reversed(self.rating) # перевёртывает рейтинг в список по убыванию баллов
    self.rating = list(enumerate(self.rating)) # онумеровывает список
    

    for pupil in self.rating:
      # (pos, [score,'username'])
      if pupil[1][1] == self.username:
        user_pos = pupil[0]
        if user_pos >= 6:
          near_pos = range(user_pos-5,user_pos+5)
        else:
          difference = user_pos-1
          near_pos = range(difference,user_pos+5)
          
        for pos in near_pos:
          self.near_rating.append(self.rating[pos])
          
    if self.near_rating == []:
      return False
    else:
      self.prettify_output()
      return True
  
  
  def parse_html(self,link):
    # функция парсинга html. по полученной ссылке отправляет GET запрос и находит в html таблицу.
    response = requests.get(link).text # GET запрос
    html = BeautifulSoup(response, 'html.parser') # форматированре в bs4
    table = html.find('table')
    trs = table.find_all('tr')[1:]
    
    # искать в каждой строке данное имя пользователя,
    # попутно сохраняя баллы детей
    for tr in trs:
      # username|achievment|math|science|english|summary
      tds = tr.find_all('td')
      score = int(tds[5].text)
      if int(score/10) == 0 and score != 0:
        score = '0' + str(score)
      
      data = [str(score),tds[0].text] # summary,username
      self.rating.append(data)
    
    

