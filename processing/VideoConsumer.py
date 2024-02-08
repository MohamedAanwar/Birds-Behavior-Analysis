from CustomEnum import Details
from CustomTime import Time
import numpy
import cv2
import threading
from Thread_basics.cls_Consumer import Cosnumer
import concurrent.futures


class VideoConsumer(threading.Thread, Cosnumer):
    def __init__(self, q, dependcisQ, excelQueue):
        super().__init__()
        self.queue = q
        self.dependcisQ = dependcisQ
        self.excelQueue = excelQueue

        self.model = self.dependcisQ.get()  # the first get will return model
        self.shape = self.dependcisQ.get()  # the second get will return the shape
        self.classes = self.dependcisQ.get()  # the third get will return the classes

    # @Override Method from abstract class
    def consume(self, q, model, classes, shape, dictFrameTime):
        try:
            while True:
                frameTuple = q.get()
                if frameTuple == None:
                    break

                frameTime = frameTuple[0]
                frame = frameTuple[1]

                new_array = cv2.resize(frame, shape)
                p = new_array.reshape(-1, shape[0], shape[1], 3)
                try:
                    predection = numpy.argmax(model.predict([p]))
                    result_frame = classes[predection]
                    dictFrameTime[frameTime] = self.get_pose(result_frame)
                except Exception as ex:
                    print(str(ex))

        except Exception as ex:
            print(ex)

    def get_pose(self, file_name):
        head = Details.head.value
        leg = Details.leg.value
        wing = Details.wing.value
        tail = Details.tail.value
        center = Details.center.value
        right = Details.right.value
        left = Details.left.value
        down = Details.down.value
        up = Details.up.value
        off = Details.off.value
        on = Details.on.value
        none = Details.none.value

        # if we take just one name
        try:
            file_name_trimmed = file_name.replace(".", ":").replace("_", ",").lower()
            file_name_trimmed = "{%s}" % file_name_trimmed
            file_name_trimmed = eval(file_name_trimmed)
            return file_name_trimmed
        except Exception as ex:
            print(str(ex))

    def get_motion_per_time(self, dict_frame_time):
        head = Details.head.value
        leg = Details.leg.value
        wing = Details.wing.value
        tail = Details.tail.value
        center = Details.center.value
        right = Details.right.value
        left = Details.left.value
        down = Details.down.value
        up = Details.up.value
        off = Details.off.value
        on = Details.on.value
        none = Details.none.value

        row = dict(
            {
                "Time": 0,
                "No Motion": "",
                "No Motion Time Span": "",
                "head status": "",
                "head movement": "",
                "head movement time span": "",
                "leg status": "",
                "leg movement": "",
                "leg movement time span": "",
                "wing status": "",
                "wing movement": "",
                "wing movement time span": "",
                "tail status": "",
                "tail movement": "",
                "tail movement time span": "",
            }
        )

        tbl_movement = []

        dict_pose_start_time = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        dict_pose_end_time = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        list_of_sorted_keys = list(sorted(dict_frame_time))
        for index, cur_time in enumerate(sorted(dict_frame_time)):
            if len(dict_frame_time) - index == 1:
                break
            else:
                # birds_curr, birds_next are the dicts representing the pose of the bird
                birds_pose_curr = dict_frame_time[cur_time]
                next_time = list_of_sorted_keys[index + 1]
                birds_pose_next = dict_frame_time[next_time]

                # if there is a diff create a new obj that contain a time
                diff = self.get_difference(birds_pose_curr, birds_pose_next)

                if len(dict_frame_time) - index == 2:
                    diff = birds_pose_next

                if diff is not None:
                    for birdPart in diff.keys():
                        # if this the second move for the same part then record the end time
                        # and caculate the time interval of the move
                        dict_pose_end_time[birdPart] = next_time

                        new_row = row.copy()
                        time = Time.formulateTime(next_time)
                        new_row["Time"] = time
                        new_row[f"{str(birdPart)} status"] = f"{diff[birdPart]}"
                        new_row[
                            f"{str(birdPart)} movement"
                        ] = f"{birds_pose_curr[birdPart]}-{diff[birdPart]}"

                        motionTime = Time.subtractTimes(
                            dict_pose_end_time[birdPart],
                            dict_pose_start_time[birdPart],
                        )
                        new_row[f"{str(birdPart)} movement time span"] = motionTime

                        if (
                            len(tbl_movement) != 0
                            and tbl_movement[len(tbl_movement) - 1]["Time"]
                            == new_row["Time"]
                        ):
                            if (
                                tbl_movement[len(tbl_movement) - 1]["head movement"]
                                == ""
                                and new_row["head movement"] != ""
                            ):
                                tbl_movement[len(tbl_movement) - 1][
                                    "head movement"
                                ] = new_row["head movement"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "head movement time span"
                                ] = new_row["head movement time span"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "head status"
                                ] = new_row["head status"]

                            if (
                                tbl_movement[len(tbl_movement) - 1]["leg movement"]
                                == ""
                                and new_row["leg movement"] != ""
                            ):
                                tbl_movement[len(tbl_movement) - 1][
                                    "leg movement"
                                ] = new_row["leg movement"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "leg movement time span"
                                ] = new_row["leg movement time span"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "leg status"
                                ] = new_row["leg status"]

                            if (
                                tbl_movement[len(tbl_movement) - 1]["wing movement"]
                                == ""
                                and new_row["wing movement"] != ""
                            ):
                                tbl_movement[len(tbl_movement) - 1][
                                    "wing movement"
                                ] = new_row["wing movement"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "wing movement time span"
                                ] = new_row["wing movement time span"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "wing status"
                                ] = new_row["wing status"]

                            if (
                                tbl_movement[len(tbl_movement) - 1]["tail movement"]
                                == ""
                                and new_row["tail movement"] != ""
                            ):
                                tbl_movement[len(tbl_movement) - 1][
                                    "tail movement"
                                ] = new_row["tail movement"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "tail movement time span"
                                ] = new_row["tail movement time span"]
                                tbl_movement[len(tbl_movement) - 1][
                                    "tail status"
                                ] = new_row["tail status"]

                        else:
                            tbl_movement.append(new_row)

                        dict_pose_start_time[birdPart] = next_time

        self.excelQueue.put(tbl_movement)
        self.excelQueue.put(None)

    def get_difference(self, first_dict, second_dict):
        try:
            first_dict = set(first_dict.items())
            second_dict = set(second_dict.items())
            return dict(second_dict - first_dict)
        except:
            return None

    def run(self):
        try:
            dictFrameTime = {}
            #  self.consume(self.queue,self.model,self.chunkSize,self.classes,self.shape)
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                for i in range(3):
                    executor.submit(
                        self.consume,
                        self.queue,
                        self.model,
                        self.classes,
                        self.shape,
                        dictFrameTime,
                    )

            self.get_motion_per_time(dictFrameTime)

        except Exception as ex:
            print(str(ex))
