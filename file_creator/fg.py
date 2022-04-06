import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from f import Ui_MainWindow
from os import *
import pyttsx3
import speech_recognition as sr
speak_engine = pyttsx3.init()
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.hello)

    def hello(self):
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            speak('Давайте уточним имя папки')
            s = r.listen(source)
        voice = r.recognize_google(s, language="ru-RU").lower()
        text = self.ui.lineEdit.text()
        chdir(text)
        mkdir(voice)
        speak('Папка создана')


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())