"""
the various_cv.py will be called by various_classify.py
"""
import os
import time
import threading
import cv2
import serial

folder = 'nano'
def show_img(img):
    assert img is not None, 'img is None'
    cv2.imshow('frame', img)
    cv2.waitKey(0)


def rotate_0_degree(img):
    return img


def rotate_90_degrees(img):
    return cv2.flip(cv2.transpose(img), 1)


def rotate_180_degrees(img):
    return cv2.flip(img, -1)


def rotate_270_degrees(img):
    return cv2.flip(cv2.transpose(img), 0)


def calculate_box_size(box):
    return int(abs(box[0] - box[-2])), int(abs(box[1] - box[-1]))


def calculate_distance(box, position=0, x_or_y='y'):
    center = [(box[0] + box[-2]) / 2, (box[1] + box[-1]) / 2]
    if x_or_y == 'x':
        return int(abs(center[0] - position))
    else:
        return int(abs(center[1] - position))


class VariousCV:
    def __init__(
            self,
            q,  # UI消息队列
            AI_module,
            cameraPath=0,
            baud_rate=9600,  # 嵌入式传输波特率
            timeout=0.5,  # 0.5秒连接超时
            serial_port_address="/dev/ttyUSB0",  # 串口位置
    ):
        self.queue = q  # 消息队列
        self.UIinformation = {
            "garbageCategory": None,
            "fullLoad": False,
            "ifSuccess": False,
            "TotalNumber": 0,
            "Kitchen waste": 0,
            "recyclable trash": 0,
            "hazardous waste": 0,
            "other garbage": 0,
            "serialOfGarbage": None,
            "ifBegin": False,
            "fullLoadGarbage": [False, False, False, False],
            "fullLoadGarbage20s": False,
            "countDown": 0,
        }
        self.name_to_type = {
            'cipian': '其他垃圾', 'eluanshi': '其他垃圾', 'tudou': '厨余垃圾', 'bailuobo': '厨余垃圾',
            'huluobo': '厨余垃圾',
            'yilaguan': '可回收垃圾', 'bottle': '可回收垃圾', 'battery': '有害垃圾', 'medician': '有害垃圾',
            'zhuankuai': '其他垃圾'
        }
        self.type_to_qinformation={
            '其他垃圾':'other garbage',
            '厨余垃圾':'Kitchen waste',
            '可回收垃圾':'recyclable trash',
            '有害垃圾':'hazardous waste'
        }
        self.cameraPath = cameraPath
        self.ser = serial.Serial(serial_port_address, baud_rate, timeout=timeout)
        self.ai_module = AI_module

        self.cap = None  # the camera
        self.img = None  # the picture by the camera

        self.type = None # the garbage type thrown down
        self.type_index = 0
        self.type_to_index = {
            '其他垃圾':0,
            '厨余垃圾':1,
            '可回收垃圾':2,
            '有害垃圾':3,
        }
        self.distance = None # the distance between the garbage and the port
    def get_img(self):
        return self.img

    def rotate(self, degree):
        switch = {
            0: rotate_0_degree,
            90: rotate_90_degrees,
            180: rotate_180_degrees,
            270: rotate_270_degrees
        }
        assert degree in switch, 'degree is not in 0,90,180,270'
        assert self.img is not None, 'img is None for rotation'
        return switch.get(degree, rotate_0_degree)(self.img)


    def open_camera(self):
        while True:
            try:
                self.cap = cv2.VideoCapture(self.cameraPath)
                self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 200)
                self.cap.set(cv2.CAP_PROP_EXPOSURE, -2)
                for i in range(2):
                    _, self.img = self.cap.read()  # read twice to wait the initiation
                self.img = self.rotate(degree=180)
                cv2.imwrite(os.path.join(folder,'img/img.png'),self.img)
                break
            except:
                print(" the camera can't be opened ")

    def close_camera(self):
        self.cap.release()
    def calculate_distance_and_size(self,names_boxes, name_to_type):
        distance = []
        for name, box_list in names_boxes.items():
            for box in box_list:
                size_and_distance = {
                    'name': name,
                    'type': name_to_type[name],
                    'size': calculate_box_size(box),
                    'distance': calculate_distance(box, position=0, x_or_y='y')
                }
                distance.append(size_and_distance)
        sorted_distance = sorted(distance, key=lambda x: x['distance'])
        return sorted_distance

    def predict(self):
        start_predict_time = time.time()
        success = self.ai_module.predict_img(self.img)

        if success:
            names_boxes = self.ai_module.get_names_boxes()
            distance = self.calculate_distance_and_size(names_boxes,self.name_to_type)
            self.type = distance[0]['type']
            self.name = distance[0]['name']
            self.type_index = self.type_to_index[self.type]
            self.distance = distance[0]['distance']
            self.UIinformation[self.type_to_qinformation[self.type]] += 1
            self.UIinformation['TotalNumber'] +=1
            self.UIinformation['garbageCategory'] = self.type
        else:
            pass
        end_predict_time = time.time()
        print(f"the predict time is {end_predict_time - start_predict_time} ,and the success is {success}")
        return success

    def send_classify_information(self):
        print("正在发送数据")
        print(self.distance)
        data = [[0x2C], [0x12], [0x00],[0x00],[0x00] ,[0x5B]]
        if self.type == "其他垃圾":
            data[2] = [0x00]
        elif self.type == "厨余垃圾":
            data[2] = [0x01]
        elif self.type == "可回收垃圾":
            data[2] = [0x02]
        elif self.type == "有害垃圾":
            data[2] = [0x03]
        else:
            print("error")
            exit()
        if self.name == 'yilaguan':
            data[3] = [0x01]
        data[4] = [int(self.distance/10)]
        for d in data:
            d = bytearray(d)
            time.sleep(0.1)
            print(d)
            self.ser.write(d)
        print("sendSerialInformation done")

    def recv(self):
        while True:
            data = self.ser.read(1)
            print(data)
            if data == b"":
                continue
            else:
                data = int.from_bytes(data, byteorder='big')
                break
        return data
    def recv_information(self):
        """
        receive the success information
        """
        # time.sleep(10)
        datas_received = [0x00,0x00,0x00]
        for index in range(len(datas_received)):
            datas_received[index] = self.recv()
        print('recv is ok:'+str(datas_received))
    def put_queue(self):
        while True:
            self.queue.put(self.UIinformation)
    def update_information_begin(self):
        self.UIinformation["ifBegin"] = True
        self.UIinformation['ifSuccess'] = False
    def update_information_over(self):
        self.UIinformation["ifBegin"] = False
        self.UIinformation['ifSuccess'] = False
    def update_information_success(self):
        self.UIinformation["ifBegin"] = True
        self.UIinformation['ifSuccess'] = True
        for i in range(50):
            self.queue.put(self.UIinformation)
    def run(self):
        put_queue_thread = threading.Thread(target=self.put_queue,args=())
        put_queue_thread.start()
        while True:
            self.open_camera()
            if self.predict():
                self.update_information_begin() # 更新开始的信息，并且将信息传送给前端
                self.close_camera()
                self.send_classify_information()
                self.recv_information()
                self.update_information_success() # 更新分类成功信息，并且将信息传送给前端
            else:
                self.close_camera()
            self.update_information_over()


if __name__ == '__main__':
    cv = VariousCV(q=None, AI_module=None)
    img = cv2.imread(r"E:\repository\yolov8_smart_can\data_test\dadianchi.png")
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv.img = img
    show_img(cv.get_img())
    img_rotate = cv.rotate(90)
    cv2.imshow('img_rotate', img_rotate)
    cv2.waitKey(0)
