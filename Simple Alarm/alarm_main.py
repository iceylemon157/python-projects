from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QEventLoop, QTimer
from alarm import Ui_MainWindow
import sys
import os
import keyboard
from time import sleep
import vlc

class WorkThread(QThread):
    sig = pyqtSignal()

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        self.sig.emit()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('sticker.png'))  # icon
        self.setWindowTitle('Anime Alarm Version 1.0')

        self.ui.start_button.clicked.connect(self.start_alarm)
        self.ui.pause_button.clicked.connect(self.pause_alarm)
        self.ui.reset_button.clicked.connect(self.reset_alarm)

        self.ui.pause_button.hide()
        self.ui.spinBox_minute.setValue(1)
        self.alarm_work = WorkThread()
        self.music_work = WorkThread()
        self.total = 0
        self.pause = False

        self.history_total = 0

        self.music = 'Nya Charging.mp3'
        self.stop_music = False

        # self.work = WorkThread()
        # self.work1 = WorkThread()
        # self.work2 = WorkThread()

    def play_music(self):
        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(self.music)
        player.set_media(media)
        player.play()
        sleep(1.5)
        duration = player.get_length() / 1000
        sleep(duration)

    def lcd_display(self):
        self.ui.lcdNumber.display(self.total // 60)
        self.ui.lcdNumber_second.display(self.total % 60)

    def Qsleep(self):
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()

    def alarm_run(self):
        print(self.total, self.pause)
        while self.total > 0 and not self.pause:
            self.lcd_display()
            self.Qsleep()
            self.total -= 1
        self.lcd_display()

        if self.total == 0:
            self.ui.pause_button.setText("TIME'S UP!")
            self.stop_music = False
            self.music_work = WorkThread()
            self.music_work.start()
            self.music_work.sig.connect(self.play_music)

            # self.stop_music = True

        print(self.total, 'time up!')

    def start_alarm(self):
        
        self.ui.pause_button.setText("pause")
        self.ui.pause_button.show()
        self.ui.reset_button.hide()
        self.ui.start_button.hide()

        if not self.pause:

            minute = self.ui.spinBox_minute.value()
            second = self.ui.spinBox_second.value()
            print(minute, second)

            self.ui.lcdNumber.display(minute)
            self.ui.lcdNumber_second.display(second)
            self.total = minute * 60 + second
            self.history_total = self.total

        self.pause = False

        print('start time', self.total)

        self.alarm_work = WorkThread()
        self.alarm_work.start()
        self.alarm_work.sig.connect(self.alarm_run)

        # self.alarm_run(minute, second)

    def pause_alarm(self):
        text = self.ui.start_button.text()
        if text == "OK!":
            self.stop_alarm()
            return

        self.pause = True
        self.ui.start_button.show()
        self.ui.pause_button.hide()
        self.ui.reset_button.show()
        minute = self.total // 60
        second = self.total % 60
        print(minute, second)

    def reset_alarm(self):
        self.pause = False
        self.ui.reset_button.hide()
        self.ui.pause_button.hide()
        self.ui.start_button.show()

        self.total = self.history_total

        print(f'history time{self.history_total}')

        self.ui.lcdNumber.display(self.total // 60)
        self.ui.lcdNumber_second.display(self.total % 60)

    def stop_alarm(self):
        self.stop_music = True


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    # keyboard.add_hotkey('enter', window.click)
    window.show()
    sys.exit(app.exec_())
