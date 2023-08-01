import os
from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto import keyboard
from pywinauto import mouse
import pyautogui
import time





class OBS:
    def __init__(self) -> None:
        self.app = Application(backend="uia")
        self.is_run = 0
    def is_running(self):
        return self.is_run   
    def run(self):
        os.chdir("C:\\Program Files\\obs-studio\\bin\\64bit\\")
        try:
            self.app.connect(path = "obs64.exe")
            self.app.Dialog.click_input()
        except:
            self.app.start('obs64.exe')
            self.app.window(best_match='OBS')

        self.is_run = 1

    def set_up_sourse(self):
        OBS.run(self)
        for i in self.app.Dialog.Dialog2.ListBox:
            f = (str(i).find('LectureRecorder'))
            if f>=0:
                return
        if f==-1:
            self.app.Dialog.Dialog2.child_window(title="Добавить", control_type="Button").click_input()
            keyboard.send_keys("{DOWN 7} {ENTER}LectureRecorder {ENTER 3}")

    def start_recording(self):
        self.app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input()
        keyboard.send_keys("{TAB 6}{SPACE}")

    def stop_recording(self):
        self.app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input()
        keyboard.send_keys("{TAB 6}{SPACE}")
    def close_app(self):
        self.app.kill()

