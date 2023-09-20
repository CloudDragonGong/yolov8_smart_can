"""
various_classify.py can classify various types of garbage
"""
import multiprocessing
from multiprocessing import Queue, Process
from PyQt5.Qt import *
import sys
from PyQt5.QtWidgets import *
from nano import various_cv
from nano import UI
from nano import yolo_module
def run_yolo(q, AI):
    AI.LoadModel()
    VM = various_cv.VariousCV(q=q,AI_module=AI)
    VM.run()

def run_UI(UIQ):
    app = QApplication(sys.argv)
    UI_object = UI.showUI(UIQ)
    UI_object.setupUi()
    app.exec_()

if __name__ == "__main__":
    # 两个用于传输信息的消息队列
    UIQ = Queue(1)
    multiprocessing.freeze_support() # windows需要加这行代码，linux不需要
    load_path = r"models/yolov8_best.onnx"
    p2 = Process(target=run_UI, args=(UIQ,))
    p2.start()
    AI = yolo_module.YoloModule(load_path=load_path)
    AI.LoadModel()
    VM = various_cv.VariousCV(cameraPath=0,q=UIQ,AI_module=AI,serial_port_address='COM3')
    VM.run()
