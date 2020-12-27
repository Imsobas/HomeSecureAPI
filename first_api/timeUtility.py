import datetime

def getDateStringFromDateTime(dateTime):
    dateTimeStr = str(dateTime)

    splits = dateTimeStr.split(" ") 
    return splits[0]
