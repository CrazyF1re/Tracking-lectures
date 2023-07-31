import os
from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto import keyboard
from pywinauto import mouse
import pyautogui
import time




os.chdir("C:\\Program Files\\obs-studio\\bin\\64bit\\")
app = Application(backend="uia").start('obs64.exe')
app.window(best_match='OBS')



def set_up_sourse():
    for i in app.Dialog.Dialog2.ListBox:
        f = (str(i).find('LectureRecorder'))
        if f>=0:
            break
    if f==-1:
        app.Dialog.Dialog2.child_window(title="Добавить", control_type="Button").click_input()
        keyboard.send_keys("{DOWN} {ENTER}LectureRecorder {ENTER}")


    app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input(button = 'right')
    keyboard.send_keys("{UP} {ENTER}")
    app.Dialog['Свойства «LectureRecorder»'].child_window(title="URL-адрес", control_type="Text").click_input()
    mouse.click(coords= pyautogui.position())
    keyboard.send_keys("{TAB 2} ")
    keyboard.send_keys("URL{TAB}")
    keyboard.send_keys("{BACKSPACE 4}1920{TAB}")
    keyboard.send_keys("{BACKSPACE 4}1080{ENTER}")

def set_url(url):
    app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input(button = 'right')
    keyboard.send_keys("{UP} {ENTER}")
    app.Dialog['Свойства «LectureRecorder»'].child_window(title="URL-адрес", control_type="Text").click_input()
    mouse.click(coords= pyautogui.position())
    keyboard.send_keys("{TAB 2} ")
    keyboard.send_keys(url+"{TAB}")

def start_recording():
    app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input()
    keyboard.send_keys("{TAB 6}{SPACE}")

def stop_recording():
    app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input()
    keyboard.send_keys("{TAB 6}{SPACE}")

#close app

time.sleep(3)

app['Dialog']['TitleBar'].child_window(title="Закрыть", control_type = "Button").click()# print_control_identifiers()
