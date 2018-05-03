from tkinter import Tk, Button, PhotoImage, Canvas
from json import JSONDecodeError
from datetime import datetime
import calendar
import time
import json
import math
import os
import pytz

class WorldClock:
    FILENAME = "dates.json"

    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width = 300, height = 300)

        self.master.title("World Clock")
        self.canvas.pack()

        self.dir = os.getcwd()
        self.photo = PhotoImage(file = self.dir + "/icon.png")
        self.button = Button(self.master, image = self.photo, command = self.showSettings)
        self.button.image = self.photo

        self.button.place(
            relx = 1.0,
            rely = 0,
            x = (-1 * math.ceil(self.photo.width() / 2)),
            y = math.ceil(self.photo.height() / 2),
            anchor = "c"
        )

        self.showDates()

    def changeTimeFormatToNumber(self, timeformat):
        times = timeformat.split(":")
        hour = int(times[0])
        minute = int(times[1])

        return hour + (minute / 60)

    def getTimeFromTimezone(self, timestamp):
        currentTime = calendar.timegm(time.gmtime())
        cet = pytz.timezone("CET")
        offset = cet.utcoffset(datetime.now())
        utc = currentTime + (3600 * (-1 * self.changeTimeFormatToNumber(str(offset))))
        date = datetime.fromtimestamp((utc + (3600 * self.changeTimeFormatToNumber(timestamp))))

        return date #.strftime("%A, %d %b, %Y %H:%M:%S")

    def showDates(self):
        try:
            handle = open(self.dir + "/" + self.FILENAME)
            content = handle.read()
            content = json.loads(content)

            for obj in content:
                self.updateCanvas(obj["city"], self.getTimeFromTimezone(obj["timezone"]))

        except (FileNotFoundError, JSONDecodeError):
            print("File Not found")

    def updateCanvas(self, city, time):
        print(city, time)

    def showSettings(self):
        print("Show Settings")

root = Tk()
app = WorldClock(root)

root.mainloop()
