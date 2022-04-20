"""
使用ffmpeg录制屏幕，并结合Pyaudio同步录制的音频合成带有声音的视频文件
"""
from pathlib import Path
from time import sleep
import sys
import ffmpeg


def file_path(filename):
    relative_path = Path('resource').joinpath(filename)
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path('.').absolute()
    return Path(base_path).joinpath(relative_path).as_posix()


class Screenshot:

    def __init__(self, width=1920, height=1080, fps=15):
        self.width = width
        self.height = height
        self.fps = fps
        self.process = None
        self.ffmpeg_path = file_path('ffmpeg.exe')

    def __call__(self, width, height, fps=None):
        self.width = width
        self.height = height
        self.fps = fps if fps else self.fps

    @staticmethod
    def unlink(filename):
        Path(filename).unlink()

    def record(self, filename, offset_x=0, offset_y=0, draw_mouse=0):
        self.process = (
            ffmpeg.output(
                ffmpeg.input(
                    filename='desktop', format='gdigrab', framerate=self.fps, offset_x=offset_x, offset_y=offset_y,
                    draw_mouse=draw_mouse, s=f'{self.width}x{self.height}'),
                filename=filename, pix_fmt='yuv420p'
            ).overwrite_output()
        )
        self.ffmpeg_async()

    def compose_audio(self, video_path, audio_path, output_path):
        self.process = (
            ffmpeg.output(
                ffmpeg.input(filename=video_path),
                ffmpeg.input(filename=audio_path),
                filename=output_path, vcodec='copy', acodec='aac', strict='experimental', pix_fmt='yuv420p'
            ).overwrite_output()
        )
        sleep(1)
        self.ffmpeg_async()

    def ffmpeg_async(self):
        self.process = self.process.run_async(cmd=self.ffmpeg_path, pipe_stdin=True, pipe_stdout=False,
                                              pipe_stderr=False)

    def terminate(self):
        if self.process is not None:
            self.process.communicate(str.encode("q"))
            self.process.terminate()
            self.process = None
