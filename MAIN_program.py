# -*- coding: utf-8 -*-
import os
import subprocess
from PyQt4 import QtGui
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import GUI
import D_Link_DIR_300
import TP_Link_TL_WA801ND
import ASUS_RT_N16


def search_and_read_file_config():
    if os.path.exists('config.txt') == False:
        er = 'Файл config.txt не найден\n' \
             'Создайте файл и заполните его построчно\n' \
             '\t1 - адрес роутера\n\t2 - логин\n\t3 - пароль\n\t4 - имя сети'
        data = ''
        return data, er
    else:
        with open('config.txt') as in_f:     #чтение из файла
            data = in_f.read().split('\n')   # data[0] - url для подключения
        in_f.closed                          # data[1] - login
                                             # data[2] - password
        for item in data:
            if item == '':
                er = 'В файле config.txt присутствуют пустые строки\n' \
                     'Удалите или заполните пустые строки и повторите попытку\n' \
                     '\t1 - адрес роутера\n\t2 - логин\n\t3 - пароль\n\t4 - имя сети'
                break
            else:
                er = ''
        return data, er


class Main(QDialog, GUI.Ui_Form ):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.workerThread_Set = WorkerThread_Set()
        self.workerThread_Timer = WorkerThread_Timer()

        self.connect(self.pushButton, SIGNAL('clicked()'), self.ComboGetItem)  # обработчик нажатия на клавишу
        self.connect(self.workerThread_Set, SIGNAL('threadDoon_IF_ERROR()'), self.IF_Error) #ожидание завершения потока с ошибкой
        self.connect(self.workerThread_Set, SIGNAL('threadDoon_IF_SUCCESS()'), self.IF_Sucsess)  # обработчик ожидания завершения потока
        self.connect(self.workerThread_Timer, SIGNAL('setTimer(int)'), self.LCD)  # смена значения таймера
        self.connect(self.workerThread_Timer, SIGNAL('threadTimerDoon'), self.IF_Sucsess_Timer_END) #сигнал для вывода в поля
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.Show_log)


    def ComboGetItem(self):
        self.groupBox.setTitle("Текщий пароль")
        self.pushButton_2.setVisible(False)
        self.label.setText('--------')
        self.label_2.setText('')
        item = self.comboBox.currentText()
        self.label_2.setText('Ждите... идет применение настроек')
        self.pushButton.setEnabled(False)
        self.comboBox.setEnabled(False)
        if item == 'ЦРБ - 192.168.16.110':
            time = 60
            self.workerThread_Set.name = 'D_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'ЦДБ - 192.168.16.50':
            time = 60
            self.workerThread_Set.name = 'D_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'ОДЛ - 192.168.1.200':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 1 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'ASUS'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 2 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 3 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 4 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 5 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 6 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 7 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 8 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 9 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 10 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 11 - 192.168.1.150':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 12 - 192.168.1.150':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 13 - 192.168.1.150':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time
        elif item == 'Филиал 14 - 192.168.1.100':
            time = 10
            self.workerThread_Set.name = 'TP_Link'
            self.workerThread_Set.start()
            self.lcdNumber.display(time)
            self.workerThread_Timer.time = time


    def IF_Error(self):
        self.label.setText(str(self.workerThread_Set.pasw))
        self.groupBox.setTitle("Текщий пароль")
        self.pushButton_2.setVisible(True)
        self.label_2.setText('Нажмите -open log file- чтобы узнать больше')
        self.pushButton.setEnabled(True)
        self.comboBox.setEnabled(True)

    def IF_Sucsess(self):
        self.lcdNumber.setVisible(True)
        self.groupBox.setTitle('Текущий пароль для ' + self.workerThread_Set.ssid)
        self.label.setText(str(self.workerThread_Set.pasw))
        self.label_2.setText('Идет перезагрузка роутера')
        self.workerThread_Timer.start()
        get_item_id = self.comboBox.currentIndex()
        ssid_pasw_f = open('ActualKey.txt', 'w')
        ssid_pasw_f.write(str(self.workerThread_Set.ssid) + '\n' +
                          str(self.workerThread_Set.pasw) + '\n' +
                          str(get_item_id))

    def IF_Sucsess_Timer_END(self):
        self.lcdNumber.setVisible(False)
        self.label_2.setText('Настройки успешно применены')
        self.pushButton.setEnabled(True)
        self.comboBox.setEnabled(True)

    def Show_log(self):
        commandLine = u'notepad.exe "log.txt"'
        subprocess.Popen(commandLine)

    def LCD(self, time):
        self.lcdNumber.display(time)


class WorkerThread_Set(QThread):
    def __init__(self, parenet=None, name=None, pasw=None, ssid=None):
        super(WorkerThread_Set, self).__init__(parenet)
        self.name = name
        self.ssid = ssid
        self.pasw = pasw

    def run(self):
        if self.name == 'D_Link':
            self.ssid, self.pasw = D_Link_DIR_300.DIR_300()
            self.check(self.pasw)
        elif self.name == 'TP_Link':
            self.ssid, self.pasw = TP_Link_TL_WA801ND.TL_WA801ND()
            self.check(self.pasw)
        elif self.name == 'ASUS':
            self.ssid, self.pasw = ASUS_RT_N16.RT_N16()
            self.check(self.pasw)

    def check(self, pasw):
        if pasw == 'ERROR':
            self.emit(SIGNAL('threadDoon_IF_ERROR()'))
        else:
            self.emit(SIGNAL('threadDoon_IF_SUCCESS()'))


class WorkerThread_Timer(QThread):
    def __init__(self, parenet=None, time=None):
        super(WorkerThread_Timer, self).__init__(parenet)
        self.time = time

    def run(self):
        while self.time > 0:
            self.time -= 1
            self.sleep(1)
            self.emit(SIGNAL('setTimer(int)'), self.time)
        self.emit(SIGNAL('threadTimerDoon'))



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())