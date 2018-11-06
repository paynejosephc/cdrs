# https://github.com/Battleroid/seccam
# Source code modified by Joseph Payne and Brandon Gill


__version__ = '0.1'

import time
#import docopt
import logging

import cv2 as cv
import imutils as im

from camera import Camera
from event import EventLoop
from threading import Thread

logging.basicConfig(level=logging.INFO)


class Sentry:
    def __init__(self, name=None, fps=10, src=0, min_area=250, noup=True, verbose=False, url=None):
        self.camera = Camera(src)
        self.loop = EventLoop(url, name=name, noup=noup, size=fps * 15, fps=fps)
        self.min_area = min_area
        self.verbose = verbose
        self.fps = fps
        self.trigger = False

    def run_loop(self):
        while True:
            frame = self.camera.read()

            # Process frame
            frame = im.resize(frame, width=300)

            if self.trigger:
                max_area = 300
            else:
                max_area = 0

            if max_area >= self.min_area:
                if not self.loop.recording:
                    logging.info('Area exceeded ({} > {}), starting capture'.format(
                        max_area, self.min_area
                    ))
                    self.loop.start_event()
                    self.loop.max_area = max_area
                    self.loop.poster_image = frame
                else:
                    self.loop.update_event()

                # Replace poster image for video if movement is larger
                if max_area is not None and max_area > self.loop.max_area:
                    self.loop.max_area = max_area
                    self.loop.poster_image = frame

            # Add frame to appropriate buffer
            self.loop.update(frame)

            # Let loop decide if it's time to finish the event
            self.loop.check_cutoff()

            # Show preview window if verbose mode is on
            if self.verbose:
                cv.imshow('Sentry', frame)
                cv.waitKey(1)

            # Sleep for an interval to achieve our desired framerate target
            time.sleep(1 / self.fps)

    def start(self):
        self.camera.start()
        time.sleep(1)

        t1 = Thread(target=self.run_loop)
        t1.setDaemon(True)
        t1.start()

    def set_trigger(self):
        print("Trigger...")
        self.trigger = True
        print("Sleep...")
        time.sleep(15)
        print("Un-trigger...")
        self.trigger = False



if __name__ == '__main__':
    # Collect args

    # Sentry related
    url = None
    name = "filename"

    # If streaming the stream first
    sentry = Sentry(name=name, verbose=True)


    # Finally start the sentry
    logging.info('Starting Sentry')
    sentry.start()

    print("Starting to sleep...")
    time.sleep(20)
    sentry.set_trigger()
