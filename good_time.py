import datetime
import pytz


current_date = datetime.datetime.now(pytz.timezone('Iran'))
current_time = current_date.strftime("%H:%M").split(":")
# print(current_time)
# print(int(current_time[0]) > 8)
# print(int(current_time[1]) > 0)
# print(int(current_time[0]) < 16)
# print(int(current_time[1]) < 7)

def good_time():
    result = False
    if( int(current_time[0]) > 8 and
        int(current_time[1]) > 0 and
        int(current_time[0]) < 16 and
        int(current_time[1]) < 7):

        result = True
    print(result)
    return result
# good_time()