import datetime

def getDateStringFromDateTime(dateTime):
    dateTime = datetime.datetime.now()
    dateTimeStr = str(dateTime)

    splits = dateTimeStr.split(" ") 
    return splits[0]
