import random
import numpy as np
import onnxruntime as ort
import cv2
from ultralytics import YOLO
from PIL import Image

def garbage_list_prediction(prediction):
    result = [prediction[int(box.cls[0])] for box in prediction.boxes.cpu().numpy()]
    return result

def garbage_numbers_prediction(prediction):
    result = {}
    for box in prediction.boxes.cpu().numpy():
        name = prediction[int(box.cls[0])]
        result[name] = 
class YoloModule:
    def __init__(self, load_path='best.onnx', cuda=False):
        self.img = None  # img
        self.img_ori = None
        self.model = None  # model
        self.providers = None  # devices
        self.load_path = load_path
        self.cuda = cuda
        self.names = ['cipian', 'eluanshi', 'tudou', 'bailuobo', 'huluobo',
                      'yilaguan', 'bottle', 'battery', 'medician']
        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.names)}

    def LoadModel(self):
        print("模型开始加载")
        self.model = YOLO(self.load_path)
        print("模型加载结束")

    def read_img(self,img):
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
        self.garbage_types = garbage_list_prediction(self.predict_result)
        self.garbage_types_numbers = garbage_numbers_prediction()

    def Module(self, frame):
        """
        the prediction function outside
        """
        im, image, ratio, dwdh = self.img_process(frame)
        outputs = self.get_preds(im)
        print(f'the length is {len(outputs)}')
        if len(outputs) == 0:
            return None
        return self.gar_sort(outputs, ratio, dwdh)

    def gar_sort(self, outputs, ratio, dwdh):
        ori_images = [self.img_ori.copy()]

        for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(outputs):
            image = ori_images[int(batch_id)]
            box = np.array([x0, y0, x1, y1])  # 框的位置坐标
            box -= np.array(dwdh * 2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()
            cls_id = int(cls_id)  # 类别id
            print(cls_id)
            score = round(float(score), 3)
            name = self.names[cls_id]  # id对应的类别
            print(name)
            color = self.colors[name]
            name += ' ' + str(score)  # 类别+概率score
            # 画框
            cv2.rectangle(image, box[:2], box[2:], color, 2)
            cv2.putText(image, name, (box[0], box[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [225, 255, 255], thickness=2)

        cv2.imwrite('img/image_anchor_frame.jpg', ori_images[0])
        pred_id = int(outputs[0][5]) + 1
        print(self.names[pred_id - 1])
        if pred_id == 1 or pred_id == 2:
            flag = 0
        elif pred_id >= 3 and pred_id <= 5:
            flag = 1
        elif pred_id >= 6 and pred_id <= 7:
            flag = 2
        elif pred_id >= 8 and pred_id <= 9:
            flag = 3
        else:
            flag = None
        print("分类完成")
        return flag, len(outputs)