#!/bin/python3

import argparse
from cpufreq import cpuFreq
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
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
# Controller
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # registration of elements events
        self.ui.applyBtn.clicked.connect(self.applyBtn_clicked)


    # ---------------events methods-------------------
    def applyBtn_clicked(self):
        pass




# View
class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(631, 499)
        Widget.setFixedSize(631, 499)

        self.tabWidget = QtWidgets.QTabWidget(Widget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 631, 521))
        self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.governorGroupBox = QtWidgets.QGroupBox(self.tab)
        self.governorGroupBox.setGeometry(QtCore.QRect(10, 10, 371, 281))
        self.governorGroupBox.setObjectName("governorGroupBox")

        self.listView = QtWidgets.QListView(self.governorGroupBox)
        self.listView.setGeometry(QtCore.QRect(10, 80, 251, 192))
        self.listView.setObjectName("listView")

        self.govLbl_2 = QtWidgets.QLabel(self.governorGroupBox)
        self.govLbl_2.setGeometry(QtCore.QRect(10, 60, 151, 19))
        self.govLbl_2.setObjectName("govLbl_2")

        self.applyGovBtn = QtWidgets.QPushButton(self.governorGroupBox)
        self.applyGovBtn.setGeometry(QtCore.QRect(270, 80, 94, 27))
        self.applyGovBtn.setObjectName("applyGovBtn")

        self.resetGovBtn = QtWidgets.QPushButton(self.governorGroupBox)
        self.resetGovBtn.setGeometry(QtCore.QRect(270, 120, 94, 27))
        self.resetGovBtn.setObjectName("resetGovBtn")

        self.govLbl_1 = QtWidgets.QLabel(self.governorGroupBox)
        self.govLbl_1.setGeometry(QtCore.QRect(10, 30, 131, 19))
        self.govLbl_1.setObjectName("govLbl_1")

        self.currGovLbl = QtWidgets.QLabel(self.governorGroupBox)
        self.currGovLbl.setGeometry(QtCore.QRect(140, 29, 131, 20))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.currGovLbl.sizePolicy().hasHeightForWidth())

        self.currGovLbl.setSizePolicy(sizePolicy)
        self.currGovLbl.setText("")
        self.currGovLbl.setObjectName("currGovLbl")

        self.freqGroupBox = QtWidgets.QGroupBox(self.tab)
        self.freqGroupBox.setGeometry(QtCore.QRect(10, 300, 611, 121))
        self.freqGroupBox.setObjectName("freqGroupBox")
        self.freqLbl = QtWidgets.QLabel(self.freqGroupBox)
        self.freqLbl.setGeometry(QtCore.QRect(180, 60, 181, 19))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freqLbl.sizePolicy().hasHeightForWidth())

        self.freqLbl.setSizePolicy(sizePolicy)
        self.freqLbl.setObjectName("freqLbl")
        self.freqHorizontalSlider = QtWidgets.QSlider(self.freqGroupBox)
        self.freqHorizontalSlider.setGeometry(QtCore.QRect(10, 80, 481, 16))
        self.freqHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.freqHorizontalSlider.setObjectName("freqHorizontalSlider")

        self.applyFreqBtn = QtWidgets.QPushButton(self.freqGroupBox)
        self.applyFreqBtn.setGeometry(QtCore.QRect(510, 40, 94, 27))
        self.applyFreqBtn.setObjectName("applyFreqBtn")

        self.resetFreqBtn = QtWidgets.QPushButton(self.freqGroupBox)
        self.resetFreqBtn.setGeometry(QtCore.QRect(510, 80, 94, 27))
        self.resetFreqBtn.setObjectName("resetFreqBtn")

        self.closeBtn = QtWidgets.QPushButton(self.tab)
        self.closeBtn.setGeometry(QtCore.QRect(520, 430, 94, 27))
        self.closeBtn.setObjectName("closeBtn")

        self.applyBtn = QtWidgets.QPushButton(self.tab)
        self.applyBtn.setGeometry(QtCore.QRect(10, 430, 94, 27))
        self.applyBtn.setObjectName("applyBtn")

        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(280, 430, 94, 27))
        self.pushButton.setObjectName("pushButton")

        self.periodGroupBox = QtWidgets.QGroupBox(self.tab)
        self.periodGroupBox.setGeometry(QtCore.QRect(390, 10, 231, 151))
        self.periodGroupBox.setObjectName("periodGroupBox")

        self.enPeriodChkBox = QtWidgets.QCheckBox(self.periodGroupBox)
        self.enPeriodChkBox.setGeometry(QtCore.QRect(10, 30, 171, 25))
        self.enPeriodChkBox.setObjectName("enPeriodChkBox")

        self.periodLbl = QtWidgets.QLabel(self.periodGroupBox)
        self.periodLbl.setEnabled(False)
        self.periodLbl.setGeometry(QtCore.QRect(10, 70, 51, 19))
        self.periodLbl.setObjectName("periodLbl")

        self.timeEdit = QtWidgets.QTimeEdit(self.periodGroupBox)
        self.timeEdit.setEnabled(False)
        self.timeEdit.setGeometry(QtCore.QRect(70, 70, 118, 28))
        self.timeEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.timeEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.timeEdit.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.timeEdit.setCalendarPopup(False)
        self.timeEdit.setObjectName("timeEdit")

        self.applyPeriodBtn = QtWidgets.QPushButton(self.periodGroupBox)
        self.applyPeriodBtn.setEnabled(False)
        self.applyPeriodBtn.setGeometry(QtCore.QRect(20, 110, 94, 27))
        self.applyPeriodBtn.setObjectName("applyPeriodBtn")

        self.resetPeriodBtn = QtWidgets.QPushButton(self.periodGroupBox)
        self.resetPeriodBtn.setEnabled(False)
        self.resetPeriodBtn.setGeometry(QtCore.QRect(130, 110, 94, 27))
        self.resetPeriodBtn.setObjectName("resetPeriodBtn")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.logPlainTextEdit = QtWidgets.QPlainTextEdit(self.tab_2)
        logPlainTextEdit_size = QtCore.QRect(10, 20, 607, 436)
        self.logPlainTextEdit.setGeometry(logPlainTextEdit_size)
        self.logPlainTextEdit.setObjectName("logPlainTextEdit")
        self.logPlainTextEdit.setUpdatesEnabled(true)
        self.logPlainTextEdit.setEnabled(false)

        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(10, 0, 72, 19))
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Widget,'GUI_CPUmode')
        self.tabWidget.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget,title_name:str):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(title_name)
        self.governorGroupBox.setTitle(_translate("Widget", "Setting governor"))
        self.govLbl_2.setText(_translate("Widget", "Available governors:"))
        self.applyGovBtn.setText(_translate("Widget", "Apply"))
        self.resetGovBtn.setText(_translate("Widget", "Cancel"))
        self.govLbl_1.setText(_translate("Widget", "Current governor:"))
        self.freqGroupBox.setTitle(_translate("Widget", "Frequency"))
        self.freqLbl.setText(_translate("Widget", "5 000 000 KHz (5.0 GHz)"))
        self.applyFreqBtn.setText(_translate("Widget", "Apply"))
        self.resetFreqBtn.setText(_translate("Widget", "Cancel"))
        self.closeBtn.setText(_translate("Widget", "Close"))
        self.applyBtn.setText(_translate("Widget", "Apply"))
        self.pushButton.setText(_translate("Widget", "Cancel"))
        self.periodGroupBox.setTitle(_translate("Widget", "Period"))
        self.enPeriodChkBox.setText(_translate("Widget", "Enable period install"))
        self.periodLbl.setText(_translate("Widget", "Period"))
        self.timeEdit.setDisplayFormat(_translate("Widget", "HH:mm:ss"))
        self.applyPeriodBtn.setText(_translate("Widget", "Apply"))
        self.resetPeriodBtn.setText(_translate("Widget", "Cancel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Widget", "Settings"))
        self.label.setText(_translate("Widget", "Log:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Widget", "Log"))



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
        app = QApplication(sys.argv)
        main_window = GUI()
        main_window.show()
        sys.exit(app.exec_())

        #gui=GUI(title='CPU