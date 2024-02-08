import os
from queue import Queue
from VideoProducer import VideoProducer
from VideoConsumer import VideoConsumer
from ExcelWriter import ExcelWriter

if __name__ == "__main__":
    model_Path = r"D:\desk\3.1\SD\Project\Model\acute egret 2nd blue object novelty TA h.h5"  # Training model path - Change to your pc path
    folder_path = r"D:\desk\3.1\SD\Project\Frames\acute egret 2nd blue object novelty TA h"  # Path for frames folder - Change to your pc path
    video_Path = r"D:\desk\3.1\SD\Project\Video\acute egret 2nd blue object novelty TA h.mp4"  # path to video - Change to your pc path
    video_name = "acute egret 2nd blue object novelty TA h"  # Video name - Change to your video name
    sheet_path = r"D:\desk\3.1\SD\Project\Model"  # Path to save excel sheet - Change to your pc path

    sheet = r"{}\{}.xlsx".format(sheet_path, video_name)

    q = Queue()
    ExcelQ = Queue()
    DependcisQ = Queue()
    shape = (128, 128)

    folder_list = []

    for folder in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, folder)):
            folder_list.append(folder)
        else:
            print("Incorrect Path !!")

    classes = folder_list

    P = VideoProducer(q, DependcisQ, video_Path, model_Path, classes, shape)
    C = VideoConsumer(q, DependcisQ, ExcelQ)
    W = ExcelWriter(ExcelQ, sheet)
    P.start()
    C.start()
    W.start()

    P.join()
    C.join()
    W.join()
