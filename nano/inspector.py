import threading
import time

import serial
folder = 'nano'
class Inspector:
    def __init__(
         self,
         q,
         baud_rate=9600,  # 嵌入式传输波特率
         timeout=0.5,  # 0.5秒连接超时
         serial_port_address="/dev/ttyUSB0"
    ):
        self.ser = serial.Serial(serial_port_address= serial_port_address,baud_rate=baud_rate,timeout=timeout)
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
        self.queue = q # 进程间的通信

    def send_data(self):
        data = [[0x5D], [0x30], [0x01], [0x2A]]
        for i in range(0, 4):
            data[i] = bytearray(data[i])
            print(data[i])
            time.sleep(0.1)
            self.ser.write(data[i])
        print("send data has done")

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

    def receive_data(self):
        data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        for i in range(len(data)):
            data[i] = self.recv()
        print(f"接收成功：{data}")
        # 5D、30、2A数据包结构
        if data[0]== 0x5D and data[1]== 0x30:
            self.UIinformation['fullLoadGarbage']=[False,False,False,False]
            for i in range(0,7):
                print(data[i])

            if data[2]==True:
                self.UIinformation['fullLoadGarbage'][0]=True
            else:
                self.UIinformation['fullLoadGarbage'][0]=False
            if data[3]==True:
                self.UIinformation['fullLoadGarbage'][1]=True
            else:
                self.UIinformation['fullLoadGarbage'][1]=False
            if data[4]==True:
                self.UIinformation['fullLoadGarbage'][2]=True
            else:
                self.UIinformation['fullLoadGarbage'][2]=False
            if data[5]==True:
                self.UIinformation['fullLoadGarbage'][3]=True
            else:
                self.UIinformation['fullLoadGarbage'][3]=False
            return True


    def update(self):
        while True:
            self.queue.put(self.UIinformation)
            time.sleep(0.035)

    def run(self):
        update_thread = threading.Thread(target=self.update)
        update_thread.start()
        while True:
            self.send_data()
            self.receive_data()
            time.sleep(10) # 每10秒检测一次
