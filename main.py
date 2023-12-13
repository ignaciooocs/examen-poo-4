import mysql.connector
import requests 

class Application:
  def __init__(self):
    self.data = []
  
  def connectDb (self):
    try:
      conn = mysql.connector.connect(
        host = 'localhost',
        user='programador',
        passwd='123456',
        database='analista',
      )
      print('Conectado a la base de datos')
      return conn
    except Exception as e:
      print(e)
    
  def convert(self):
    url = 'https://raw.githubusercontent.com/panchojarab/iap/main/preES4'
    resultado = requests.get(url)
    if resultado.status_code == 200:
      data = resultado.json()
      for item in data['ResultSet']['Result']:
        self.data.append(
          {
            'title': item['Title'],
            'fileSize': item['FileSize'],
            'summary': item['Summary'],
            'url': item['Thumbnail']['Url']
          }
        )

      self.mostrar_info()
  
  def mostrar_info(self):
    if self.data == []:
      print('No hay resultados')
      return
    for item in self.data:
      print('title: ', item['title'])
      print('fileSize: ', item['fileSize'])
      print('summary: ', item['summary'])
      print('url: ', item['url'])
      print('\n')

  def add_to_database(self):
    if self.data == []:
      print('No hay resultados')
      return
    conn = self.connectDb()
    cursor = conn.cursor()
    try:
      for item in self.data:
        query = 'insert into preparaciones (title, fileSize, summary, url) values(%s, %s, %s, %s)'
        data = (item['title'], item['fileSize'], item['summary'], item['url'])
        cursor.execute(query, data)
      conn.commit()
      conn.close()
      print('Se insertó correctamente a la base de datos')
    except Exception as e:
      print(e)
      print('Error al insertar a la base de datos')

  def main(self):
    while True:
      response = input('Selecciona una opción: ')
      if response == '1':
        self.convert()
      elif response == '2':
        self.mostrar_info()
      elif response == '3':
        self.add_to_database()
      elif response == '4':
        break



app = Application()
app.main()


