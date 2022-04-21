# 使用python动手做一个屏幕录制工具  

*更新日期：2022-04-20*  
> windows 10  
> python 3.7

- Screeshot_Gui.exe [84.0M] [下载地址](https://github.com/lk-itween/FunnyCodeRepository/releases/download/Screenshot_Gui/Screenshot_Gui.exe)  
将ffmpeg一并打包在exe文件中，且使用pyinstaller打包，生成文件较大  

- Screenshot_Gui.py  
pyqt5制作的屏幕录制窗口，窗口程序入口

- Screenshot_record.py  
使用ffmpeg工具，利用python调用ffmpeg命令行来录制屏幕

- Audio_record.py  
pyaudio读取可录制音频设备，设定需要使用的设备进行录制音频

- Screenshot_record_with_cv2.py  
使用opencv-python录制视频并保存

- Screenshot_test.py  
无窗口化测试联动屏幕录制及音频录制，保持音视频同时录制和同时停止录制

- resource
保存程序运行过程中需要使用到的程序或图片

- requirements.txt  
已将所需模块放在requirements.txt中，可直接pip install requirements.txt下载安装。  


**ps:**  
*1. ffmpeg.exe 请至此https://www.gyan.dev/ffmpeg/builds/#release-builds 下载符合的版本，并解压将bin下的ffmpeg.exe移动到resource文件夹下*  
*2. 如果PyAudio包不能使用pip在线安装，python3.7环境请下载PyAudio-0.2.11-cp37-cp37m-win_amd64.whl至本地，在该路径下打开cmd窗口，执行pip install 该whl文件*  
*3. 其他python环境可在https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio 下自行安装对应版本的whl文件*  

