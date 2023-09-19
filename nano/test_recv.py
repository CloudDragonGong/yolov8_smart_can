import cv2

# 创建摄像头对象
cap = cv2.VideoCapture(1)  # 0表示默认摄像头，如果有多个摄像头，可以尝试不同的编号

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 设置视频窗口的尺寸
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

while True:
    # 读取一帧视频
    ret, frame = cap.read()

    # 检查是否成功读取帧
    if not ret:
        print("无法读取帧")
        break

    # 显示视频帧
    cv2.imshow("Camera", frame)

    # 检测按键事件，按下'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()

# 关闭所有窗口
cv2.destroyAllWindows()
