from pyaudio import PyAudio, paInt16, paContinue, paComplete
import wave
from threading import Thread
import time
from pathlib import Path


class AudioRecord(PyAudio):

    def __init__(self, channels=2):
        super().__init__()
        self.chunk = 1024  # 每个缓冲区的帧数
        self.format_sample = paInt16  # 采样位数
        self.channels = channels  # 声道： 1，单声道；2，双声道
        self.fps = 44100  # 采样频率
        self.input_dict = None
        self.output_dict = None
        self.stream = None
        self.filename = '~test.wav'
        self.wf = None
        self.stop_flag = False
        self.kill = False

    def callback_input(self, in_data, frame_count, time_info, status):
        """录制回调函数"""
        self.wf.writeframes(in_data)
        if not self.stop_flag:
            return (in_data, paContinue)
        else:
            return (in_data, paComplete)

    def callback_output(self, in_data, frame_count, time_info, status):
        """播放回调函数"""
        data = self.wf.readframes(frame_count)
        return (data, paContinue)

    def open_stream(self, name):
        """打开录制流"""
        input_device_index = self.get_device_index(name, True) if name else None
        return self.open(format=self.format_sample,
                         channels=self.channels,
                         rate=self.fps,
                         frames_per_buffer=self.chunk,
                         input=True,
                         input_device_index=input_device_index,
                         stream_callback=self.callback_input
                         )

    def audio_record_run(self, name=None):
        """音频录制"""
        self.wf = self.save_audio_file(self.filename)
        self.stream = self.open_stream(name)
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.1)
        self.wf.close()
        if self.kill:
            Path(self.filename).unlink()
        self.duration = self.get_duration()
        self.terminate_run()

    def run(self, filename=None, name=None, record=True):
        """音频录制启动"""
        if record:
            if filename:
                self.filename = filename
            thread_1 = Thread(target=self.audio_record_run, args=(name,))
        else:
            if not filename:
                raise Exception('未输入音频文件名，不能播放，请输入后再试！')
            thread_1 = Thread(target=self.read_audio, args=(filename, name,))
        thread_1.start()

    def read_audio(self, filename, name=None):
        """音频播放"""
        output_device_index = self.get_device_index(name, False) if name else None
        with wave.open(filename, 'rb') as self.wf:
            # 获取音频长度
            self.duration = self.get_duration()
            self.stream = self.open(format=self.get_format_from_width(self.wf.getsampwidth()),
                                    channels=self.wf.getnchannels(),
                                    rate=self.wf.getframerate(),
                                    output=True,
                                    output_device_index=output_device_index,
                                    stream_callback=self.callback_output
                                    )
            self.stream.start_stream()
            while self.stream.is_active():
                time.sleep(0.1)
        print(self.duration)
        self.terminate_run()

    def get_duration(self):
        """获取音频时长"""
        return round(self.wf.getnframes() / self.wf.getframerate(), 2)

    def get_in_out_devices(self):
        """获取系统输入输出设备"""
        self.input_dict = {}
        self.output_dict = {}
        for i in range(self.get_device_count()):
            devinfo = self.get_device_info_by_index(i)
            if not devinfo['hostApi'] and int(devinfo['defaultSampleRate']) == self.fps \
                    and '映射器' not in devinfo['name']:
                if devinfo['maxInputChannels']:
                    self.input_dict[devinfo['name'].split(' ')[0]] = i
                elif devinfo['maxOutputChannels']:
                    self.output_dict[devinfo['name'].split(' ')[0]] = i

    def get_device_index(self, name, inp=True):
        """获取选定设备索引"""
        if inp and self.input_dict:
            return self.input_dict.get(name, -1)
        elif not inp and self.output_dict:
            return self.output_dict.get(name, -1)

    def save_audio_file(self, filename):
        """音频文件保存"""
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.get_sample_size(self.format_sample))
        wf.setframerate(self.fps)
        return wf

    def terminate_run(self):
        """结束流录制或流播放"""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = None
        self.wf = None
        self.terminate()
