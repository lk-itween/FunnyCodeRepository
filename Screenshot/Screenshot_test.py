from threading import Thread
from pynput import keyboard  # pip install pynput
from Audio_record import AudioRecord
from Screenshot_record import Screenshot


def hotkey():
    """热键监听"""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def on_press(key):
    try:
        video.terminate()
        if key.char == 't':  # t键，录制结束，保存音视频
            audio.stop_flag = True
        elif key.char == 'k':  # k键，录制中止，删除文件
            audio.stop_flag = True
            audio.kill = True
            video.unlink('test.mp4')
    except Exception as e:
        print(e)


key_thread = Thread(target=hotkey, daemon=True)
audio = AudioRecord()
video = Screenshot()
key_thread.start()
audio.run(filename='test.mp3')
video.record('test.mp4')
