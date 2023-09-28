# 本项目指南

## nano目录结构

~~~shell
.
├── AI_module.py
├── IFlytek.py
├── SparkApi.py
├── UI.py
├── cv_module.py
├── docs
│   ├── answers.txt
│   ├── keywords.txt
│   └── questions.txt
├── img
│   ├── 1.jpg
│   ├── 1.mov
│   ├── 1.mp4
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   ├── 5.png
│   ├── Image.jpg
│   ├── a.png
│   ├── b.png
│   ├── c.png
│   ├── cutOutPicture.jpg
│   ├── d.png
│   ├── e.png
│   ├── edge1.jpg
│   ├── f.png
│   ├── frame.jpg
│   ├── g.png
│   ├── h1.png
│   ├── h2.png
│   ├── h3.png
│   ├── h4.png
│   ├── image_anchor_frame.jpg
│   ├── img.png
│   ├── imgOut.jpeg
│   ├── mask.jpg
│   └── pictureForAI.jpg
├── inspector.py
├── lock.py
├── test_recv.py
├── test_send.py
├── various_cv.py
├── voice
│   ├── recording.mp3
│   ├── recording.wav
│   ├── recordning.wav
│   ├── response.mp3
│   └── response.wav
├── voice_assitant
│   ├── VoiceAssistant.py
│   ├── __init__.py
│   ├── parsing_MP3.py
│   ├── prompt.py
│   ├── real_time_recording_of_audio.py
│   ├── response.py
│   ├── stt.py
│   ├── tts.py
│   └── voice_assistant_stupid.py
└── yolo_module.py
~~~

## 核心代码

### 根目录

> 本项目是基于yolov8，添加了nano文件夹及其所有文件，以及根目录下的python运行脚本：
>
> - classify.py : 分类单个垃圾
> - full_inspection.py:单独进行满载检测
> - Various_classify.py:分类多个垃圾
>
> 这几个都不是屎山代码

### nano目录下

nano中还有一些关于智能语音有关的文件，对于工训赛来说并没有什么鸟用

- cv_module.py：
  大二写的屎山代码，需要阅读代码，建议重写

- various_cv.py：
	不是屎山代码，建议拿来用，可拓展性高
	
- yolo_module.py：
	分类器，不是屎山代码，拓展性强
	
- UI.py：
	屎山代码，但是建议不要重写，没什么很大的bug，就是阅读起来相当困难，效果还是挺好看的

  [youtube链接](https://www.youtube.com/watch?v=mjIxYqITBE4)

[摄像头曝光](https://blog.csdn.net/m0_63230414/article/details/133394588?spm=1001.2014.3001.5501)





