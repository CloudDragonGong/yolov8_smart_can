"""
various_classify.py can classify various types of garbage
"""
import multiprocessing
from multiprocessing import Queue, Process
from PyQt5.Qt import *
import sys
from PyQt5.QtWidgets import *
from nano import UI
from nano.inspector import Inspector

def run_UI(UIQ):
    app = QApplication(sys.argv)
    UI_object = UI.showUI(UIQ)
    UI_object.setupUi()
    app.exec_()

if __name__ == "__main__":
    # 两个用于传输信息的消息队列
    UIQ = Queue(1)
    multiprocessing.freeze_support() # windows需要加这行代码，linux不需要
    process_UI = multiprocessing.Process(target=run_UI,args=(UIQ,))
    process_UI.start()
    inspector = Inspector(q = UIQ,serial_port_address='COM3')
    inspector.run()