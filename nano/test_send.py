import serial
import time

garbageType = "其他垃圾"

ser = serial.Serial(
    port='COM3',  # 串口端口，根据你的实际情况修改
    baudrate=9600,  # 波特率，根据你的串口设备配置修改
    timeout=None  # 读取超时时间，设置为None表示一直等待数据
)
def sendSerialInformation():
    print("正在发送数据")

    data = [[0x2C], [0x12], [0x00], [0x5B]]
    if garbageType == "其他垃圾":
        data[2] = [0x00]
    elif garbageType == "厨余垃圾":
        data[2] = [0x01]
    elif garbageType == "可回收垃圾":
        data[2] = [0x02]
    elif garbageType == "有害垃圾":
        data[2] = [0x03]
    else:
        print("error")
        exit()
    for i in range(0, 4):
        data[i] = bytearray(data[i])
        time.sleep(0.1)
        print(data[i])
        ser.write(data[i])
    print("sendSerialInformation done")
def recv():
    while True:
        print('begin')
        data = ser.read(1)
        print(data)
        if data == b"":
            continue
        else:
            break
    return data

if __name__  ==  '__main__':
    sendSerialInformation()
