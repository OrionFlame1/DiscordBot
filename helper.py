import datetime
import checkFreeGames

def timestamp():
    time = str(datetime.datetime.now())
    return '[' + time[time.find(" ") + 1:time.find('.')] + ']'

# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
#     }

def getEpicGames():
    return checkFreeGames.getEpicGames()

def seconds_to_format(secs):
    secs = int(secs)
    res = ""
    hours = 0
    mins = 0
    if secs >= 3600:
        while secs >= 3600:
            hours += 1
            secs -= 3600
    if secs >= 60:
        while secs >= 60:
            mins += 1
            secs -= 60
    if hours > 0:
        res += f"{hours}h "
    if mins > 0:
        res += f"{mins}m "
    if secs > 0:
        res += f"{secs}s "
    return res
