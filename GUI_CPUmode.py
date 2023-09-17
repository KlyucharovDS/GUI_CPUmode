#!/bin/python3

from tkinter import *
from tkinter.messagebox import *
import argparse
from pprint import pprint
from cpufreq import cpuFreq
from time import sleep
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSpinBox, QSlider, QComboBox, QLabel
from PyQt5.QtCore import Qt
true = True
false = False


def getCPUmodes()->list:
    return ['conservative', 'ondemand', 'userspace', 'powersave', 'performance', 'schedutil']

class CPU:
    __cpu = None
    __fmax = 0
    __fmin = 0
    @staticmethod
    def init():
        CPU.__cpu = cpuFreq()
        # CPU.__cpu.reset()
        CPU.__cpu.disable_hyperthread()
        CPU.__fmax = CPU.get_freq()
        CPU.__fmin = CPU.__fmax.copy()
        # CPU.__cpu.set_governors("powersave")
        # print(CPU.get_cpu_modes())
        # time.sleep(0.1)

    # def __init__(self):
    #     self.__cpu = cpuFreq()
    #     self.__cpu.reset()
    #     self.__cpu.disable_hyperthread()
    @staticmethod
    def get_available_modes() -> list:
        return CPU.__cpu.available_governors

    @staticmethod
    def get_cpu_modes() -> list:
        return list(CPU.__cpu.get_governors().values())

    @staticmethod
    def set_cpu_mode( mode:str):
        CPU.__cpu.set_governors(mode)
        time.sleep(0.1)

    @staticmethod
    def get_available_freq()-> list:
        return CPU.__cpu.available_frequencies

    @staticmethod
    def get_freq()->list:
        return list(CPU.__cpu.get_frequencies().values())

    @staticmethod
    def set_freq( freq:int):
        """
        freq in KHz
        :param freq:
        :return:
        """
        CPU.set_max_freq(freq)
        CPU.set_min_freq(freq)
        #CPU.__cpu.set_frequencies(freq)

    @staticmethod
    def set_max_freq(freq:int):
        CPU.__fmax = [freq for _ in range(CPU.get_cpu_online())]
        for i in range(CPU.get_cpu_online()):
            if CPU.__fmax[i] < CPU.__fmin[i]:
                CPU.__fmin[i] = CPU.__fmax[i]
        CPU.__cpu.set_max_frequencies(freq,rg=CPU.__cpu.get_online_cpus())
        time.sleep(0.1)

    @staticmethod
    def set_min_freq(freq:int):
        CPU.__fmin = [freq for _ in range(CPU.get_cpu_online())]
        for i in range(CPU.get_cpu_online()):
            if CPU.__fmax[i] < CPU.__fmin[i]:
                CPU.__fmax[i] = CPU.__fmin[i]
        CPU.__cpu.set_min_frequencies(freq,rg=CPU.__cpu.get_online_cpus())
        time.sleep(0.1)

    @staticmethod
    def destructor():
        pass

    @staticmethod
    def get_cpu_online()->int:
        return len(CPU.__cpu.get_online_cpus())

    @staticmethod
    def get_max_freq():
        return CPU.__fmax

    @staticmethod
    def get_min_freq():
        return CPU.__fmin

class GUI:


    def __init__(self, title:str, freq_values:list):
        # Создаем экземпляр приложения
        self.__app = QApplication(sys.argv)

        # Создаем главное окно (QWidget)
        self.__window = QWidget()
        self.__window.setWindowTitle(title)
        self.__window.setGeometry(100, 100, 400, 500)
        self.__window.setFixedHeight(500)
        self.__window.setFixedWidth(400)

        # добавляем элементы управления
        self.__closeBtn = QPushButton('Close', self.__window)
        self.__closeBtn.setGeometry(250, 145, 90, 30)
        self.__applyBtn = QPushButton('Apply', self.__window)
        self.__applyBtn.setGeometry(50, 145, 90, 30)
        # QSlider + QLaber
        self.__freq = QSlider(Qt.Horizontal, self.__window)
        self.__freq.setSingleStep(100000)
        freq_values.sort()
        self.__freq.setMinimum(freq_values[0])
        self.__freq.setMaximum(freq_values[-1])
        x = 50
        y = 50
        w = 300
        h = 10
        self.__freq.setGeometry(x,y,w,h)
        self.__freq_label0 = QLabel(self.__window)
        self.__freq_label0.setGeometry(x+(w-x)/2,y-25,120,20)
        self.__freq_label0.setText(str(self.__freq.value()))
        self.__freq_label0.show()
        self.__freq.show()

        # Подключаем обработчик события к кнопке
        self.__closeBtn.clicked.connect(self.__on_button_click)
        self.__freq.valueChanged.connect(self.__move)

        # Отображаем окно
        self.__window.show()

        # Запускаем главный цикл приложения
        self.__exit()

    # Создаем обработчик события для кнопки
    def __on_button_click(self):
        self.__exit()

    def __move(self):
        self.__freq_label0.setText(str(self.__freq.value()))


    def __exit(self,status=None):
        if status:
            sys.exit(status)
        else:
            sys.exit(self.__app.exec_())




def get_max_min_freq_def()->dict:
    freq = CPU.get_freq()
    max_min_dict ={}
    max_min_dict['max'] = freq
    max_min_dict['min'] = freq
    return max_min_dict

def info():
    print('Full info:')
    regime = CPU.get_cpu_modes()
    freq = CPU.get_freq()
    n_cpu = CPU.get_cpu_online()
    for i in range(1, n_cpu + 1):
        print('\t', str(i) + ')', regime[i - 1],'freq =',freq[i - 1], 'KHz (max =', CPU.get_max_freq()[i - 1], 'KHz,' ' min =',
              CPU.get_min_freq()[i - 1], 'KHz)')

def set_cpu_state_perm(period:int, freq=None,mode=None):
    """
    :param period: период проверки состояния процессора и установки необходимого в сек
    :return:
    """
    while true:
        if mode is not None:
            modes = CPU.get_cpu_modes()
            for m in modes:
                if m != mode:
                    CPU.set_cpu_mode(mode)
                    print(f'set mode: {mode}')
        if freq is not None:
            curr_freq = CPU.get_max_freq()
            if curr_freq != freq:
                CPU.set_max_freq(freq)
                print(f'set frequency: {freq}KHz')
        time.sleep(period)


def check_limit(value):
    """
    Check limit of inputing value
    :param value:
    :return:
    """
    limit = 3600
    if 0.1 <= int(value) <= limit:
        raise argparse.ArgumentTypeError(f"Value will must from 0 to {limit} seconds")
    return int(value)






if "__main__" == __name__:
    CPU.init()
    avail_modes = CPU.get_available_modes()
    avail_freq =  CPU.get_available_freq()
    #-----------configuration arguments-----------
    arg = argparse.ArgumentParser(prog='GUI_CPUmode')
    arg.add_argument('-m','--set_mode', type=str,choices=avail_modes, required =false, dest='set_mode',
                     help = 'set cpu mode(governor)')
    arg.add_argument('-f', '--set_freq', type=int, choices=avail_freq,required =false, dest='set_freq',
                     help = 'set current frrquency in KHz')
    arg.add_argument('-p', '--period', required=false, type=check_limit,dest='period',
                     help='[0.1,3600] sec.  period check and set cpu state. If this argument is used, then the '
                          'application checks the current state of the processor each period_seconds and sets their '
                          'parameters if they have changed.'
                          'You may exit from application then will press "q" key.', )
    arg.add_argument('--fmax', type=int, choices=avail_freq, required =false, dest = 'fmax',help='max frequency in KHz')
    arg.add_argument('--fmin', type=int, choices=avail_freq, required =false, dest = 'fmin',help='min frequency in KHz')
    arg.add_argument('--get_freq',required =false, action='store_true',
                     dest='get_freq',help='available frequency of target CPU')
    arg.add_argument('--get_mode', required=false, action='store_true',
                     dest='get_mode',help='available regime of target CPU')
    arg.add_argument('--info', required=false, action='store_true',dest='info',
                     help='print full information about CPUs')
    arg = arg.parse_args()
    #---------------args handling--------------------
    # set mode
    if arg.set_mode:
        CPU.set_cpu_mode(arg.set_mode)
    # set current frequency
    if arg.set_freq:
        CPU.set_freq(arg.set_freq)
    # set period update
    if arg.period:
        set_cpu_state_perm(arg.period, freq=arg.set_freq, mode=arg.set_mode)
        pass
    # set freq max
    if arg.fmax:
        CPU.set_max_freq(arg.fmax)
    # set freq min
    if arg.fmin:
        CPU.set_min_freq(arg.fmin)
    # get freq
    if arg.get_freq:
        freq = CPU.get_freq()
        print('Frequences:')
        count = 0
        for f in freq:
            count += 1
            print('\t',str(count) + ')',f, 'KHz (max =',CPU.get_max_freq()[count-1],'KHz,'
                ' min =', CPU.get_min_freq()[count-1],'KHz)' )
    # get regime
    if arg.get_mode:
        print('Regime:')
        regime = CPU.get_cpu_modes()
        count = 0
        for r in regime:
            count += 1
            print('\t',str(count)+')', regime[count-1])

    # get full information about CPUs
    if arg.info or arg.set_mode or arg.set_freq:
       info()

    # GUI
    if len(sys.argv) == 1:
        gui=GUI(title='CPU mode',freq_values=CPU.get_available_freq())








