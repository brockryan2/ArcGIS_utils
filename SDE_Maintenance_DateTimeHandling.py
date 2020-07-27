import datetime

class CustomDateTime(object):

    print("Assigning date/time variables...")

    date = None
    time = None

    def __init__(dateTimeObject_day, dateTimeObject_month, dateTimeObject_year, dateTimeObject_hour, dateTimeObject_minute, dateTimeObject_second, self, *args, **kwargs):
        date = str(dateTimeObject_year)
        time = ''

        def checkMonthLength(self, dateTimeObject_month):
            # if the month number is less than 10 -->
            if(int(month) < 10):
                # then a leading "0" gets assigned to the "monthString" variable
                monthString = "0"
                # then the month number is appended, useful for making 1 into 01 which is more human-readable in a file name
                monthString = monthString + (str(month))
                # otherwise, the two-digit month number gets cast from an int to a String, then is assigned to the "monthString"   variable
            else: monthString = str(month)

            date = date + '-' + monthString
        
        
        def checkDayLength(self, dateTimeObject_day):
            if(int(day) < 10):  
                    # then a leading "0" gets assigned to the "dayString" variable
                    dayString = "0"  
                    # then the day of the month is appended, useful for making 1 into 01 which is more human-readable in a file name
                    dayString = dayString + (str(day))  
                # otherwise, the two-digit day gets cast from an int to a String, then is assigned to the "dayString" variable
            else: dayString = str(day)

            date = date + '-' + dayString
            
            
        def checkHourLength(self, dateTimeObject_hour):
            # if the hour number is less than 10 -->
            if(int(hour) < 10):
                # then a leading "0" gets assigned to the "hourString" variable
                hourString = "0"
                # then the hour number is appended, useful for making 1 into 01 which is more human-readable in a file name
                hourString = hourString + (str(hour))
            # otherwise, the two-digit hour number gets cast from an int to a String, then is assigned to the "hourString"     variable
            else: hourString = str(hour)

            time = hourString


        def checkMinuteLength(self, dateTimeObject_minute):
            # if the minute number is less than 10 -->
            if(int(minute) < 10):
                # then a leading "0" gets assigned to the "minuteString" variable
                minuteString = "0"
                # then the minute number is appended, useful for making 1 into 01 which is more human-readable in a file name
                minuteString = minuteString + (str(minute))
            # otherwise, the two-digit minute number gets cast from an int to a String, then is assigned to the "minuteString"     variable
            else: minuteString = str(minute)

            time = time + ':' + minuteString


        def checkSecondLength(self, dateTimeObject_second):
            # if the second number is less than 10 -->
            if(int(second) < 10):
                # then a leading "0" gets assigned to the "secondString" variable
                secondString = "0"
                # then the second number is appended, useful for making 1 into 01 which is more human-readable in a file name
                secondString = secondString + (str(second))
            # otherwise, the two-digit second number gets cast from an int to a String, then is assigned to the "secondString"     variable
            else: secondString = str(second)

            time = time + ':' + secondString

        checkDayLength(dateTimeObject_day)
        checkMonthLength(dateTimeObject_month)

        checkHourLength(dateTimeObject_hour)
        checkMinuteLength(dateTimeObject_minute)
        checkSecondLength(dateTimeObject_second)