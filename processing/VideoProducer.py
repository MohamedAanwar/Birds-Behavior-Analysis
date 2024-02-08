import cv2
import tensorflow as tf
import threading
from Thread_basics.cls_Producer import Producer
import concurrent.futures


class VideoProducer(threading.Thread, Producer):
    def __init__(self, q, dependicesQ, videoPath, modelPath, classes, shape):
        try:
            super().__init__()
            self.queue = q
            self.videoCapture = cv2.VideoCapture(videoPath)
            self.model = tf.keras.models.load_model(modelPath)
            self.dependicesQ = dependicesQ
            self.classes = classes
            self.shape = shape

            self.dependicesQ.put(self.model)  # put the model
            self.dependicesQ.put(self.shape)  # put the shape
            self.dependicesQ.put(self.classes)  # put the classes

        except Exception as ex:
            print(str(ex))

    # @Override Method from abstract class
    def produce(self, q, videoStream):
        try:
            count = 1
            while True:
                ret, frame = videoStream.read()

                if not ret:
                    break

                if count % 15 == 0:
                    frameTime = videoStream.get(cv2.CAP_PROP_POS_MSEC)
                    q.put((frameTime, frame))

                count += 1

            videoStream.release()
            cv2.destroyAllWindows()
            print("finish sending all the frames")
            q.put(None)
            q.put(None)
            q.put(None)
        except Exception as ex:
            print(str(ex))

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.produce, self.queue, self.videoCapture)
