import os
import pandas as pd
import numpy as np
from CustomTime import Time
import threading
from Thread_basics.cls_Readucer import Readucer
import concurrent.futures


class ExcelWriter(threading.Thread, Readucer):
    def __init__(self, excelQueue, sheetPath):
        super().__init__()
        self.excelQueue = excelQueue
        self.sheetPath = sheetPath
        self.DictTotalTIme = {}

    def TotalTimeCalc(self, df, sheetPath):
        def get_body_part_time(df, part_name):
            movement_column = f"{part_name} movement"
            time_column = f"{part_name} movement\n time span"
            part_df = (
                df[[movement_column, time_column]].dropna().sort_values(movement_column)
            )
            part_df[movement_column] = part_df[movement_column].apply(
                lambda x: x.split("-")[0]
            )
            part_df[time_column] = part_df[time_column].apply(Time.reverseFormulateTime)
            sum_part = part_df.groupby(movement_column).sum()
            total = sum_part[time_column].sum()
            sum_part = sum_part[time_column].apply(Time.formulateTime)
            data = list(
                zip([part_name] * sum_part.size, sum_part.index, sum_part.values)
            )
            data.append((part_name, "total", Time.formulateTime(total)))
            return data

        try:
            data = []
            for part in ["head", "leg", "wing", "tail"]:
                data.extend(get_body_part_time(df, part))

            data = pd.DataFrame(
                data, columns=["Body Part", "Status", "Total Time"]
            ).set_index("Body Part")

            with pd.ExcelWriter(
                sheetPath, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                data.to_excel(writer, sheet_name="Total Time Statistcs")

        except Exception as ex:
            print(str(ex))

    def MovementCountCalc(self, df):
        parts_list = []
        sum_all_body = 0
        for part in ["head", "leg", "wing", "tail"]:
            counts = df[f"{part} movement"].value_counts()

            body_part = [part] * (counts.size + 1)
            movements = list(counts.keys()) + ["total"]
            sum_part = sum(counts.values)
            sum_all_body += sum_part
            values = list(counts.values) + [sum_part]

            data = zip(body_part, movements, values)
            parts_list += list(data)

        parts_list.append(("all body", "", sum_all_body))

        export_details = pd.DataFrame(
            parts_list, columns=["Body Part", "Movement", "Count"]
        ).set_index("Body Part")

        with pd.ExcelWriter(
            self.sheetPath, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:
            export_details.to_excel(writer, sheet_name="Movements Count")

    def readuce(self, changeq, sheetPath):
        try:
            while True:
                change = changeq.get()
                # print(change)
                if change == None:
                    break

                export_details = pd.DataFrame(change).set_index("Time")

                export_details.columns = [
                    "No Motion",
                    "No Motion\n Time Span (sec)",
                    "head status",
                    "head movement",
                    "head movement\n time span",
                    "leg status",
                    "leg movement",
                    "leg movement\n time span",
                    "wing status",
                    "wing movement",
                    "wing movement\n time span",
                    "tail status",
                    "tail movement",
                    "tail movement\n time span",
                ]

                if not os.path.exists(self.sheetPath):
                    with pd.ExcelWriter(sheetPath, engine="openpyxl") as writer:
                        export_details.to_excel(writer, sheet_name="Details")
                else:
                    with pd.ExcelWriter(
                        sheetPath,
                        engine="openpyxl",
                        mode="a",
                        if_sheet_exists="overlay",
                    ) as writer:
                        export_details.to_excel(
                            writer,
                            sheet_name="Details",
                            startrow=writer.sheets["Details"].max_row,
                            header=False,
                        )

                export_details.replace("", np.nan, inplace=True)
                self.TotalTimeCalc(export_details, sheetPath)
                self.MovementCountCalc(export_details.iloc[:-1])
                print("EcelWriter: Exporting data done succesfully.")
        except Exception as ex:
            print(ex)

    def run(self):
        self.readuce(self.excelQueue, self.sheetPath)
