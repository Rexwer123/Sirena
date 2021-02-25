import pyttsx3
import speech_recognition as sr
from flexx import flx
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
        saySomething('Произошла ошибка при распозновании речи')

def listDevices():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Микрофон: {1}\nИндекс: {0}\n".format(index, name))

    microphoneIndex = input('Индекс желаемого устройства ввода: ')
    return microphoneIndex


if __name__ == "__main__": #Выолнить код секции, если main.py был запущен как скрипт
    index = int(listDevices())
    while True:
        recordVolume(index) #запись индекса желаемого устройства ввода

