"""
credits for this part of the code come from:
http://blog.miguelgrinberg.com/post/video-streaming-with-flask
"""

import time
import io
import threading
import gevent


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    picamera = None

    def __init__(self):
        self.initialize()

    def initialize(self):
        if Camera.thread is None:
            print "getting camera"
            if Camera.picamera is None:
                Camera.picamera = __import__('picamera')
            # start background frame thread
            # Camera.thread = gevent.thread.start_new_thread(self._thread)
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.setDaemon(True)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0.01)
            print "eerste beeld gevonden"

    def get_frame(self):
        Camera.last_access = time.time()
        # self.initialize()
        return self.frame


    @classmethod
    def _geventThread(cls):
        print "pawning gevent thread"
        thread = gevent.spawn(cls._thread)
        thread.join()

    @classmethod
    def _thread(cls):
        print "thread started"
        with Camera.picamera.PiCamera() as camera:
            # camera setup
            print "camera gevonden"
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            print "let camera warm up"
            camera.start_preview()
            print "preview started"
            time.sleep(2)
            print "from now on there are pictures"
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()
                #print "new frame available"

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
                # gevent.sleep()
                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    pass
                    # break
        # cls.thread = None


class ECamera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    def get_frame(self):
        return self.frames[int(time.time()) % 3]
