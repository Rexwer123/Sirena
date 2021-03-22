import pyttsx3
import speech_recognition as sr
from pymongo import MongoClient
from pymongo.objectid import ObjectId

#------Начало конфигурации синтезатора речи------

tts = pyttsx3.init()
rate = tts.getProperty('rate')
tts.setProperty('rate', rate-40)

volume = tts.getProperty('volume')
tts.setProperty('volume', volume+0.9)

voices = tts.getProperty('voices')


tts.setProperty('voice', 'ru') 

for voice in voices:
    if voice.name == 'Anna':
        tts.setProperty('voice', voice.id)

#------Конец конфигурации синтезатора речи------

#------Абстрактный класс для синхронного взаимодействия и по классу для каждой бд------

class mongoClass:
    def __init__(self):
        self.client = client

    def addMacross(self, name, activationPhrase, hasParentControl, pathToExecutable, appType):
        #activationPhrase <STRING> - фраза активации, которую распознаватель речи будет отлавливать для запуска макросса
		#hasParentControl <BOOLEAN> - имеет ли макросс ограничения по использованию при включённом родительском контроле
		#pathToExecutable <STRING> - путь к испольняемому приложению, которое будет запускать макросс
		#appType <STRING> (выбирается из выпадающего списка: браузер, текстовый редактор и тд.) - тип приложения, запускаемого макроссом. Нужно для предопределения поведения программы при работе с различными типами приложений
		#Проверить, существует ли макрос
        try:
            query = self.client.db("Sirena").collection("Macrosses").find_one({
				"name": name,
				"activationPhrase": activationPhrase,
				"pathToExecutable": pathToExecutable,
			})
            if query != Null:
                #сказать, что макросс уже существует
                print("[X] Макросс уже существует!")
            else:
                #добавить макросс в бд
                self.client.db("Sirena").collection("Macrosses").inseret_one({
                    "name": name,
                    "activationPhrase": activationPhrase,
                    "hasParentControl": hasParentControl,
                    "pathToExecutable": pathToExecutable,
                    "appType": appType
                })
        except:
            print("[X] Невозможно установить соединение с бд")
        else:
            print("[OK] Макросс успешно добавлен")

    def deleteMacross(self, id):
        try:
            self.client.db("Sirena").collection("Macrosses").delete_one({
                "_id": ObjectID(id)
            })
        except:
            print("[X] Невозможно установить соединение с бд")
        else:
            print("[OK] Макросс успешно удалён.")
    
    def changeUserPreferences(self, key, value):
        #Изменение пользовательских настроек
        try:
            self.client.db("Sirena").collection("Preferences").update_one({
                "name": key
            },{
                "$set": {
                    "value": value
                }
            })
        except:
            print("[X] Невозможно установить соединение с бд")
        else:
            print("[OK] Настройки успешно обновлены")
    
    def nuke(self):
        #Возвращение к заводским настройкам (очистка бд)
        try:
            self.client.db("Sirena").collection("Macrosses").delete_many({})
            self.client.db("Sirena").collection("Preferences").delete_many({})
        except:
            print("[X] Невозможно установить соединение с бд")
        else:
            print("[OK] Настройки и макроссы были успешно сброшены")

#Абстрактный класс DB для синхронной работы со всеми базами данных, необходимо для нормального режима работа приложения
class db:
    def __init__(self):
        #Инициализация (создание экземпляров классов для работы с каждой бд)
        self.mongo = mongoClass()
	    #self.sql
	    #self.neoforge

    def addMacross(self, name, activationPhrase, hasParentControl, pathToExecutable, appType):
        #Добавить макросс
        self.mongo.addMacross(name, activationPhrase, hasParentControl, pathToExecutable, appType)
        #self.sqlClient.addMacross(name, activationPhrase, hasParentControl, pathToExecutable, appType)
        #self.neoforge.addMacross(name, activationPhrase, hasParentControl, pathToExecutable, appType)
    
    def deleteMacross(self, id):
        #Удалить макросс
        self.mongo.deleteMacross(id)
        #self.sql.deleteMacross(id)
        #self.neoforge.deleteMacross(id)
        
    def changeUserPreferences(self, key, value):
        #Изменить пользовательские настройки
        self.mongo.changeUserPreferences(key, value)
        #self.sql.changeUserPreferences(key, value)
        #self.neoforge.changeUserPreferences(key, value)

    def nuke(self):
        self.mongo.nuke()
        #self.sql.changeUserPreferences(key, value)
        #self.neoforge.changeUserPreferences(key, value)

    def closeDBConnections(self):
        self.mongo.closeDBConnections()
        #self.sql.closeDBConnections()
        #self.neoforge.closeDBConnections()

def saySomething(string): #Функция для синтеза речи из желаемой строки
    tts.say(string)
    tts.runAndWait()

def recordVolume(index): #Функция для определения сказанной фразы, необходимо решить проблему с доступом к микрофону
    r = sr.Recognizer()
    with sr.Microphone(device_index = index) as source:
        saySomething('Подавляю шум')
        r.adjust_for_ambient_noise(source, duration=0.5) #настройка подавления фоновых шумов
        saySomething('Слушаю')
        audio = r.listen(source)
    saySomething('Услышала')
    try:
        query = r.recognize_google(audio, language = 'ru-RU')
        text = query.lower()
        saySomething('Вы сказали: {query.lower()}')
    except:
        saySomething('Произошла ошибка при распознавании речи')

def listDevices():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Микрофон: {1}\nИндекс: {0}\n".format(index, name))

    microphoneIndex = input('Индекс желаемого устройства ввода: ')
    return microphoneIndex




if __name__ == "__main__": #Выолнить код секции, если main.py был запущен как скрипт
    index = int(listDevices())
    while True:
        recordVolume(index) #запись индекса желаемого устройства ввода