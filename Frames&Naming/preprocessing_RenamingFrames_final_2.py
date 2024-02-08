from threading import *
import cv2
import os
import queue
from tkinter import Tk
from tkinter.filedialog import *
from tkinter import messagebox

NO_Frames = 0


class Producer(Thread):
    def __init__(self, path, q, SecondCounter):
        super().__init__()
        self.path = path
        self.queue = q
        self.FrameCounter = SecondCounter

    def run(self):
        stream = cv2.VideoCapture(str(self.path))
        FPS = int(stream.get(cv2.CAP_PROP_FPS))
        self.FrameCounter *= FPS
        NO_Frames = stream.get(cv2.CAP_PROP_FRAME_COUNT)

        i = 0
        while i < int(self.FrameCounter):
            stream.read()
            i += 1

        while True:
            success, image = stream.read()
            if self.FrameCounter % FPS == 0:
                print(self.FrameCounter)
              
                self.queue.put(image)
            self.FrameCounter += 1
            if self.FrameCounter == NO_Frames or success == False:
                break


class Consumer(Thread):
    def __init__(self, q, path, SecondCounter):
        super().__init__()
        self.q = q
        self.path = path
        self.SecondCounter = SecondCounter

    def run(self):
        count = self.SecondCounter
        last = None
        while True:
            img = self.q.get()
            img = cv2.resize(img, (405, 720))
            count += 1
            cv2.imshow(f"Image {str(count).zfill(4)}", img)

            name = ""

            key = cv2.waitKeyEx(0)

            if key == ord("l") and last != None:
                name = last
            else:
                name += self.head(key, True)
                name += self.leg()
                name += self.wing()
                name += self.tail()

         

            images_path = str(self.path)[:-4]
            category_path = str(self.path)[:-4] + "\\" + name

            if not os.path.exists(images_path):
                os.makedirs(images_path)

            if not os.path.exists(category_path):
                os.makedirs(category_path)

            cv2.imwrite(
                category_path + "\\" + str(count).zfill(4) + str(name) + ".jpg",
                img,
            )
            cv2.destroyWindow(f"Image {str(count).zfill(4)}")
            print(f"Saved : {str(count).zfill(4) + name}.jpg")
            last = name
            f = open(path_text_last_file, "w")
            f.write(str(count))
            f.close()

            if count == NO_Frames:
                break

    def head(self, key, is_first):
        if not is_first:
            key = cv2.waitKeyEx(0)

        if key == 2424832:
            return "Head.Left"  # Left
        elif key == 2490368:
            return "Head.Center"  # Up  => Center
        elif key == 2555904:
            return "Head.Right"  # Right
        elif key == 13:
            return "Head.None"  # Enter = None
        elif key == ord("q") or key == -1:
            print("Closing .... ")
            exit()
        else:
            messagebox.showerror("Error", "Please Enter Valid Key")
            return self.head(key, False)

    def leg(self):
        key = cv2.waitKeyEx(0)
        if key == 2490368:  # Up = Leg Up
            return "_Leg.Up"
        elif key == 2621440:  # Down = Leg Down
            return "_Leg.Down"
        elif key == 13:  # Enter = None
            return "_Leg.None"
        elif key == ord("q") or key == -1:
            print("Closing .... ")
            exit()
        else:
            messagebox.showerlror("Error", "Please Enter Valid Key")
            return self.leg()

    def wing(self):
        key = cv2.waitKeyEx(0)
        if key == 2490368:
            return "_Wing.On"  # Up = Wing On
        elif key == 2621440:
            return "_Wing.Off"  # Down = Wing Off
        elif key == 13:
            return "_Wing.None"  # Enter = Wing None
        elif key == ord("q") or key == -1:
            print("Closing .... ")
            exit()
        else:
            messagebox.showerror("Error", "Please Enter Valid Key")
            return self.wing()

    def tail(self):
        key = cv2.waitKeyEx(0)
        if key == 2424832:  # Left = Tail left
            return "_Tail.Left"
        elif key == 2490368:  # Up = Tail Center
            return "_Tail.Center"
        elif key == 2555904:  # Right = Tail Right
            return "_Tail.Right"
        elif key == 13:  # Enter = Tail None
            return "_Tail.None"
        elif key == ord("q") or key == -1:
            print("Closing .... ")
            exit()
        else:
            messagebox.showerror("Error", "Please Enter Valid Key")
            return self.tail()


if __name__ == "__main__":
    q = queue.Queue()

    fpath = askopenfilename()
    path_text_last_file = "D:/desk/3.1/SD/Project/last.txt"
    f = open(path_text_last_file, "r")

    try:
        SC = int(f.read())
    except:
        SC = 0

    f.close()

    P = Producer(fpath, q, SC)
    P.start()
    c = Consumer(q, fpath, SC)
    c.start()
