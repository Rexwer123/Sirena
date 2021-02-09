import pyttsx3
import speech_recognition as sr

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

if __name__ == "__main__": #Выолнить код секции, если main.py был запущен как скрипт
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Микрофон: {1}\nИндекс: {0}\n".format(index, name))

    microphoneIndex = input('Индекс желаемого устройства ввода: ') #запись индекса желаемого устройства ввода