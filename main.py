import pyttsx3
import speech_recognition as sr
from pymongo import MongoClient
from bson.objectid import ObjectId


#------Начало конфигурации синтезатора речи------

tts = pyttsx3.init()
rate = tts.getProperty('rate')
tts.setProperty('rate', 210)

volume = tts.getProperty('volume')
tts.setProperty('volume', volume+0.9)

voices = tts.getProperty('voices')


tts.setProperty('voice', 'en') 

for voice in voices:
    print(voice)
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
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
    
    def closeDBConnections(self):
        self.client.close()

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



class Sirena:
    def __init__(self):
        self.r = sr.Recognizer()

    def saySomething(self, string): #Функция для синтеза речи из желаемой строки
        tts.say(string)
        tts.runAndWait()

    def sayHello(self): #Sirena: Привет!
        self.saySomething('Hello!')

    def sayCantUnderstant(self): #Sirena: Не понимаю
        self.saySomething("Sorry, I can't understand")

    def sleep(self): #Завершить работу приложения
        self.saySomething("Goodnight")
        exit()

    def commandIdentification(self, command):
        if command == 'sleep':
            self.goToSleep()
        if command == 'hello':
            self.sayHello()
        else:
            self.sayCantUnderstant()

    def recognizeUserCommand(self):
        with sr.Microphone() as source:
            self.r.pause_threshold = 0.5
            self.r.adjust_for_ambient_noise(source, duration=0.25)
            audio = self.r.listen(source)
        try:
            command = self.r.recognize_google(audio).lower()

            if 'execute' in command:
                self.commandIdentification(command.split("execute ")[1])

        except sr.UnknownValueError:
            print('[X] UnknownValueError Exception')

if __name__ == "__main__": #Выолнить код секции, если main.py был запущен как скрипт
    sirena = Sirena()
    while True:
        sirena.recognizeUserCommand() #запись индекса желаемого устройства ввода