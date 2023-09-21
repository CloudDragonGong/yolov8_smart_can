import serial
import time
ser = serial.Serial('COM3',9600,timeout=0.5)
data = [[0x2C], [0x12], [0x01],[0x01],[0x10], [0x5B]]

for i in range(len(data)):
    data[i] = bytearray(data[i])
    time.sleep(0.1)
    print(data[i])
    ser.write(data[i])
print("sendSerialInformation done")

# def recv():
#     while True:
#         data = ser.read(1)
#         print(data)
#         if data == b"":
#             continue
#         else:
#             break
#     return data
#
#
# data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00]
#
# print('开始等待读取')
# for i in range(0,7):
#     data[i]=recv()
#     data[i]=int.from_bytes(data[i],byteorder='big')
#     print(data[i])
# print('读取完成')

