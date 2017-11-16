import sys
from PyQt5 import QtCore, QtWidgets

class AThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        thread_func()


def thread_func():
    print("Thread works")
    timer = QtCore.QTimer()
    timer.timeout.connect(timer_func)
    timer.start(1000)
    print(timer.remainingTime())
    print(timer.isActive())

def timer_func():
    print("Timer works")

app = QtWidgets.QApplication(sys.argv)
thread_instance = AThread()
thread_instance.start()
thread_instance.exec_()
sys.exit(app.exec_())
