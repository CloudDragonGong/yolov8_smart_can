import multiprocessing
from multiprocessing import Queue, Process
from PyQt5.Qt import *
import sys
from PyQt5.QtWidgets import *
from nano import AI_module
from nano import cv_module
from nano import UI


# UI显示的字典 测试使用
UIinformation = {
    "garbageCategory": None,
    "fullLoad": False,
    "ifSuccess": False,
    "TotalNumber": 0,
}

# 运行视觉模块  测试使用
def run_VM(q, AI):
    AI.LoadModel()
    VM = cv_module.Vision_Module(q=q,AI_module=AI)
    VM.run()


# 运行UI模块
def run_UI(UIQ):
    app = QApplication(sys.argv)
    UI_object = UI.showUI(UIQ)
    UI_object.setupUi()
    app.exec_()


if __name__ == "__main__":
    # 两个用于传输信息的消息队列
    UIQ = Queue(1)
    voice_assistant_communication_queue = Queue(1)
    multiprocessing.freeze_support() # windows需要加这行代码，linux不需要
    load_path = r"E:\repository\model\yolov7.onnx"
    p2 = Process(target=run_UI, args=(UIQ,))
    p2.start()
    AI = AI_module.AIModule(load_path=load_path)
    AI.LoadModel()
    VM = cv_module.Vision_Module(cameraPath=1,q=UIQ,AI_module=AI,voice_assistant_communication_queue=voice_assistant_communication_queue,serial_port_address='COM3')
    VM.run()
    
    
