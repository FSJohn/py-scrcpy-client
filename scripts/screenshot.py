from time import time
import scrcpy
from adbutils import adb
import threading
import cv2

class Screen:
    def __init__(self):
        # set devices
        items = [i.serial for i in adb.device_list()]
        device = adb.device(items[0])

        # setup client
        self.client = scrcpy.Client(
                device=device,
                bitrate=1000000000,
            )
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
        
        # data
        self.img = None

        # threading
        th = threading.Thread(target=self.start,daemon=True) 
        th.start()

    def on_frame(self,frame):
        if frame is not None:
            self.img = frame

    def screenshot(self):
        while True:
            if self.img is not None:
                cv2.imwrite("test.jpg",self.img)
                return self.img

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()



if __name__ == "__main__":
    import time
    phone = Screen()
    for _ in range(100):
        start = time.time()
        phone.screenshot()
        end = time.time()
        print("using:{:.8f}s".format(end-start))
    phone.stop()


