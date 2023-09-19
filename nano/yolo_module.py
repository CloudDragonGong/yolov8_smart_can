import random
import numpy as np
import cv2
from ultralytics import YOLO


def name_list_prediction(prediction):
    result = [prediction[int(box.cls[0])] for box in prediction.boxes.cpu().numpy()]
    return result


def name_numbers_boxes_prediction(prediction):
    result_numbers = {}
    result_boxes = {}
    for box in prediction.boxes.cpu().numpy():
        name = prediction[int(box.cls[0])]
        if name not in result_numbers:
            result_numbers[name] = 0
        result_numbers[name] += 1
        result_boxes[name] = box
    return result_numbers, result_boxes


def type_list_prediction(name_list, name_to_type):
    garbage_type_list = [name_to_type[name] for name in name_list]
    return garbage_type_list


def type_numbers_prediction(name_numbers, name_to_type):
    name_numbers = {name_to_type[name]: number for name, number in name_numbers.items()}
    return name_numbers


def type_boxes_prediction(names_boxes, name_to_type):
    type_boxes = {name_to_type[name]: box for name, box in names_boxes.items()}
    return type_boxes


class YoloModule:
    def __init__(self, load_path='best.onnx', cuda=False):
        self.type_boxes = None
        self.garbage_type_numbers = None
        self.garbage_type = None
        self.names_boxes = None
        self.garbage_names_numbers = None
        self.garbage_names = None
        self.predict_result = None
        self.img = None  # img
        self.img_ori = None
        self.model = None  # model
        self.providers = None  # devices
        self.load_path = load_path
        self.cuda = cuda
        self.names = ['cipian', 'eluanshi', 'tudou', 'bailuobo', 'huluobo',
                      'yilaguan', 'bottle', 'battery', 'medician']
        self.name_to_type = {
            'cipian': '其他垃圾', 'eluanshi': '其他垃圾', 'tudou': '厨余垃圾', 'bailuobo': '厨余垃圾',
            'huluobo': '厨余垃圾',
            'yilaguan': '可回收垃圾', 'bottle': '可回收垃圾', 'battery': '可回收垃圾', 'medician': '有害垃圾',
            'zhuantou': '其他垃圾'
        }
        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.names)}

    def LoadModel(self):
        print("模型开始加载")
        self.model = YOLO(self.load_path)
        print("模型加载结束")

    def read_img(self, img):
        """
        read the img and copy img_ori
        """
        self.img = img
        self.img_ori = img.copy()

    def predict(self):
        """
        predict the result:
        - the garbage type list of prediction
        - the dict {garbage type : num}
        - the dict {garbage type : box}
        - the garbage name list of prediction
        - the dict {garbage name : num}
        - the dict {garbage name : box}
        """
        self.predict_result = self.model(self.img)[0]
        self.garbage_names = name_list_prediction(self.predict_result)
        self.garbage_names_numbers, self.names_boxes = name_numbers_boxes_prediction(self.predict_result)
        self.garbage_type = type_list_prediction(self.garbage_names, self.name_to_type)
        self.garbage_type_numbers = type_numbers_prediction(self.garbage_names_numbers, self.name_to_type)
        self.type_boxes = type_boxes_prediction(self.names_boxes, self.name_to_type)

    def Module(self, frame):
        """
        the prediction function outside
        """
        return self.garbage_type[0],self.garbage_type_numbers[self.garbage_type[0]]
