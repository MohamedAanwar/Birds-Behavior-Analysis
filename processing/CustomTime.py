class Time(object):
    """Represents the time of day.
    attributes: minute, second
    """

    def __init__(self, hours=0, minutes=0, seconds=0, milis=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milis = milis

    @staticmethod
    def formulateTime(time):
        # time is a time in millisecound
        totalsecound = time / 1000
        minutes = int(totalsecound / 60)
        secondsAndmillis = totalsecound % 60
        return f"{minutes}:{secondsAndmillis:.3f}"

    @staticmethod
    def subtractTimes(time2, time1):
        # method to subtract times in milli secounds
        time = time2 - time1
        return Time.formulateTime(time)

    @staticmethod
    def reverseFormulateTime(formulatedTime):
        # formulatedTime is a string in the format "minutes:seconds.milliseconds"
        minutes, secondsAndMillis = formulatedTime.split(":")
        seconds, milliseconds = secondsAndMillis.split(".")
        totalSeconds = int(minutes) * 60 + int(seconds)
        totalTimeInMillis = totalSeconds * 1000 + int(milliseconds)
        return totalTimeInMillis


if __name__ == "__main__":
    print(Time.formulateTime(60812))
    print(Time.subtractTimes(9812, 1245))
    print(Time.reverseFormulateTime("1:0.812"))
