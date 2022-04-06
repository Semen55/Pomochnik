# Голосовой ассистент Кейсон 1.0 BETA
from os import *
import os
import webbrowser
import g
import speech_recognition as sr
from fuzzywuzzy.fuzz import ratio
import pyttsx3
import datetime
import subprocess
# настройки
opts = {
    "alias": ("кейсон","кейс","кайсон","кайс","кейси","куйсон","тайсон","джейсон","казино","песня","кессон","козино","пейсон"),
    "tbr": ("скажи","расскажи","покажи","сколько","произнеси","включи","активируй","подключи",),
    "cmds": {
        "ctime": ("текущее время", "сейчас времени", "который час"),
        "files": ("найди файл", "открой файл", "мне нужен файл"),
        "folder": ("создай папку", "сделай папку"),
        "workspace": ("активируй воркспэйс", "воркспэйс","запусти воркспейс"),
        "work_add": ("создай воркспэйс", "добавь воркспэйс", "мне нужен новый воркспейс"),
        "searcher": ("что ты знаешь про", "что такое"),
    }
}

# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            speak("Слушаю вас")
        # обращаются к Кейсону
        cmd = voice

        for x in opts["alias"]:
            cmd = cmd.replace(x, "").strip()

        for x in opts["tbr"]:
            cmd = cmd.replace(x, "").strip()

        # распознаем и выполняем команду
        cmd1 = cmd
        cmd = recognize_cmd(cmd)
        execute_cmd(cmd["cmd"], cmd1)

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

# Распознование
def recognize_cmd(cmd):
    RC = {"cmd": "", "percent": 50}
    for c, v in opts["cmds"].items():

        for x in v:
            vrt = ratio(cmd, x)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt

    return RC

# Выполнение команды
def execute_cmd(cmd,cmd1):

    if cmd == "ctime":
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + " часов "+ " : " + str(now.minute)+ " минут")

    elif cmd == "files":
        # файл
        speak("Давайте уточним имя файла")
        file_name = input()
        for root, dirs, files in os.walk("C:/"):
            for name in files:
                if name.endswith(file_name):
                    webbrowser.open(os.path.join(root, name))
                    continue
                else:
                    continue
    elif cmd == "folder":
       parent_dir = os.path.dirname(os.path.abspath(__file__))
       parent_dir = parent_dir.replace("dist\caison", "")
       subprocess.Popen(os.path.join(parent_dir, "file_creator\\dist\\fg\\fg.exe"))
       # Папки на рабочем столе
    elif cmd == "searcher":
       # поиск в интернете
       webbrowser.open("https://yandex.ru/search/?lr=66&text=" + cmd1.split()[-1] + "&src=suggest_Pers")
    elif cmd == "workspace":
       # workspase
       g.call()
    elif cmd == "work_add":
       # создание воркспейсов
       parent_dir = os.path.dirname(os.path.abspath(__file__))
       parent_dir = parent_dir.replace("dist\caison", "")
       subprocess.Popen(os.path.join(parent_dir, 'work\\dist\\g\\g.exe'))
    else:
        print("Команда не распознана, повторите!")

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
# voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[4].id)
speak("Кейсон слушает")
# for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
# stop_listening(wait_for_stop=False)
while True:
    with m as source:
        audio = r.listen(source)
    callback(r, audio)  # infinity loop
