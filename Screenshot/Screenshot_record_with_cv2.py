import time
from PIL import ImageGrab
import cv2
from pathlib import Path
import numpy as np
from numba import jit
from pynput import keyboard
from threading import Thread


@jit(nopython=True)
def average_n(x, y):
    """Numpy计算趋近值"""
    return ((x + y + y) // 3).astype(x.dtype)


class ScreenshotVideo(Thread):

    def __init__(self, width, high, path='', fps=15):
        """初始化参数"""
        super().__init__()
        self.save_file = path
        self.best_fps = fps
        self.fps = fps
        self.width = width
        self.high = high
        self.spend_time = 1
        self.flag = False
        self.kill = False
        self.video = None

    def __call__(self, path):
        """重载视频路径，便于类的二次调用"""
        self.save_file = Path(path)
        self.video = self.init_videowriter(self.save_file)

    @staticmethod
    def screenshot():
        """静态方法，屏幕截图，并转换为np.array数组"""
        return np.array(ImageGrab.grab())

    @staticmethod
    def get_fourcc(name):
        """视频编码字典"""
        fourcc_maps = {'.avi': 'I420',
                       '.m4v': 'mp4v',
                       '.mp4': 'avc1',
                       '.ogv': 'THEO',
                       '.flv': 'FLV1',
                       }
        return fourcc_maps.get(name)

    def init_videowriter(self, path):
        """获取视频编码并新建视频文件"""
        if not path:
            raise Exception('视频路径未设置，请设置\nvideo = ScreenshotVideo(fps,width,high)\nvideo = video(video_path)')
        path = Path(path) if isinstance(path, str) else path
        fourcc = cv2.VideoWriter_fourcc(*self.get_fourcc(path.suffix))
        return cv2.VideoWriter(path.as_posix(), fourcc, self.fps, (self.width, self.high))

    def video_record_doing(self, img):
        """将BGR数组转换为RGB数组"""
        im_cv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.video.write(im_cv)

    def video_record_end(self):
        """录制结束，根据条件判断文件是否保存"""
        self.video.release()
        cv2.destroyAllWindows()
        if self.save_file and self.kill:
            Path(self.save_file).unlink()

    def video_best_fps(self, path):
        """获取电脑录制视频的最优帧率"""
        video = cv2.VideoCapture(path)
        fps = video.get(cv2.CAP_PROP_FPS)
        count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.best_fps = int(fps * ((int(count) / fps) / self.spend_time))
        video.release()

    def pre_video_record(self):
        """预录制，以获取最佳fps值"""
        self.video = self.init_videowriter('test.mp4')
        start_time = time.time()
        for _ in range(10):
            im = self.screenshot()
            self.video_record_doing(im)
        self.spend_time = round(time.time() - start_time, 4)
        self.video_record_end()
        time.sleep(2)
        self.video_best_fps('test.mp4')
        Path('test.mp4').unlink()

    def insert_frame_array(self, frame_list):
        """Numpy增强截图信息"""
        fps_n = round(self.fps / self.best_fps)
        if fps_n <= 0:
            return frame_list
        times = int(np.log2(fps_n))  # 倍率
        for _ in range(times):
            frame_list2 = map(average_n, [frame_list[0]] + frame_list[:-1], frame_list)
            frame_list = [[x, y] for x, y in zip(frame_list2, frame_list)]
            frame_list = [j for i in frame_list for j in i]
        return frame_list

    def frame2video_run(self):
        """使用opencv将连续型截图转换为视频"""
        self.video = self.init_videowriter(self.save_file)
        start_time = time.time()
        frame_list = []
        while True:
            frame_list.append(self.screenshot())
            if self.flag:
                break
        self.spend_time = round(time.time() - start_time, 4)
        if not self.kill:  # 视频录制不被终止将逐帧处理图像
            frame_list = self.insert_frame_array(frame_list)
            for im in frame_list:
                self.video_record_doing(im)
        self.video_record_end()

    def hotkey(self):
        """热键监听"""
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            if key.char == 't':  # 录屏结束，保存视频
                self.flag = True
            elif key.char == 'k':  # 录屏中止，删除文件
                self.flag = True
                self.kill = True
        except Exception as e:
            print(e)

    def run(self):
        # 运行函数
        # 设置守护线程
        Thread(target=self.hotkey, daemon=True).start()
        # 运行截图函数
        self.frame2video_run()


screen = ImageGrab.grab()
width, high = screen.size
video = ScreenshotVideo(width, high, fps=60)
video.pre_video_record()  # 预录制获取最优fps
video('test1.mp4')
video.run()
