import os
from pywinauto.application import Application
from pywinauto import keyboard


class OBS:
    def __init__(self) -> None:
        self.app = Application(backend="uia")

    def make_active(self):
        self.app.Dialog.click_input()

    def run(self):
        os.chdir("C:\\Program Files\\obs-studio\\bin\\64bit\\")
        try:
            self.app.connect(path = "obs64.exe")
            self.app.Dialog.click_input()
        except:
            self.app.start('obs64.exe')
            self.app.window(best_match='OBS')

    def set_up_sourse(self):
        self.make_active()
        for i in self.app.Dialog.Dialog2.ListBox:
            f = (str(i).find('LectureRecorder'))
            if f>=0:
                return
        if f==-1:
            self.app.Dialog.Dialog2.child_window(title="Добавить", control_type="Button").click_input()
            keyboard.send_keys("{DOWN} {ENTER}LectureRecorder {ENTER 1} {TAB 6} 1920 {TAB} 1080 {ENTER}")
                
    def set_url(self,url):
        self.make_active()
        for i in self.app.Dialog.Dialog2.ListBox:
            f = (str(i).find('LectureRecorder'))
            if f>=0:    
                self.app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input(button='right')
                keyboard.send_keys("{UP} {ENTER} {TAB 5}"+url+"{ENTER}")
                return

    def start_recording(self):
        self.make_active()
        self.app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input()
        keyboard.send_keys("{TAB 6}{SPACE}")

    def stop_recording(self):
        self.make_active()
        self.app.Dialog.Dialog2.child_window(title="LectureRecorder", control_type="ListItem").click_input()
        keyboard.send_keys("{TAB 6}{SPACE}")

    def close_app(self):
        self.app.kill()

