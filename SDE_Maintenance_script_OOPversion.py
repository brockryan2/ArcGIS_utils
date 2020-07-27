#################################################################################################################################
#                                                                                                                               #
#                                                       SDE MAINTENANCE                                                         #
#                                                RECONCILE, POST && COMPRESS                                                    #
#                                                                                                                               #
#################################################################################################################################

# coding: utf-8

#################################################################################################################################
#                                                                                                                               #
#                     *Recommended*: Run the "SDE Version Diagnostics" script before running this script.                       #
#                 This will check for inconsistencies in the delta (A and D) tables of a versioned geodatabase                  #
#                                                                                                                               #
#################################################################################################################################


# ===============================================================================================================================

#################################################################################################################################

#                                                         BEGIN SCRIPT:

print("Staring script...\n....\n ")

#################################################################################################################################

#                                                        IMPORT MODULES:

print("Importing modules...")

import datetime
import time

script_start_time = datetime.datetime.now()

import arcpy    # Essential: to run any of the esri functions/methods called within this script
import os

 from subprocess import Popen

 print("...module imports complete!\n ")


 #################################################################################################################################

#                                                  DATE HANDLING/FORMATTING:

print("Assigning date/time variables...")

today = datetime.date.today() # method to get the current date, assigning it to the variable "today"

day   = today.day             # assigns the day portion of today's date to the "day" variable
month = today.month           # assigns the month portion of today's date to the "month" variable
year  = today.year            # assigns the year portion of today's date to the "year" variable

dayString   = ''              # creates an empty String variable for the day that will be used later
monthString = ''              # creates an empty String variable for the day that will be used later
yearString  = str(year)       # casts the year variable from int to String and assigns it to the "yearString" variable


# Functions to encapsulate the methods to check if the day/month portions of the date are less than 10.
# These don't have to be encapsulated in functions, but it is a better practice from an OOP standpoint

# the day and dayString variables get passed into the function
def checkDayLength(day, dayString):
     # if the day of the month is less than 10 -->
	if(int(day) < 10):
         # then a leading "0" gets assigned to the "dayString" variable
		dayString = "0"
        # then the day of the month is appended, useful for making 1 into 01 which is more human-readable in a file name
		dayString = dayString + (str(day))
     # otherwise, the two-digit day gets cast from an int to a String, then is assigned to the "dayString" variable
	else: dayString = str(day)

	return dayString  # returns the "dayString" variable back to the method that called it


# the month and monthString variables get passed into the function
def checkMonthLength(month, monthString):
     # if the month number is less than 10 -->
	if(int(month) < 10):
         # then a leading "0" gets assigned to the "monthString" variable
		monthString = "0"
         # then the month number is appended, useful for making 1 into 01 which is more human-readable in a file name
		monthString = monthString + (str(month))
     # otherwise, the two-digit month number gets cast from an int to a String, then is assigned to the "monthString" variable
	else: monthString = str(month)

	return monthString  # returns the "monthString" variable back to the method that called it

print("....\n ")

# Function/method calls to transform the current date into a human readable date format for use in file(path) names
dayString = checkDayLength(day, dayString)          # this calls the above defined "checkDayLength" function
monthString = checkMonthLength(month, monthString)  # this calls the above defined "checkMonthLength" function
# Variable to concatenate the String versions of the "day" "month" and "year" variable into the folowing format: YYYYMMDD
todayString = yearString + "-" + monthString + "-" + dayString

print("....done assigning date/time variables!\n ")

################################################################################################################################

#                                    DEFINE VARIABLES THAT ARE DEPENDENT ON THE DATE FUNCTIONS:

def makeMaintenanceDirectory():
	print("Making directory for logs...")

	if(!os.direxists(os.path.join(SDE_maintenance_folderPath, "Update_" + todayString))):

		os.mkdir(os.path.join(SDE_maintenance_folderPath, "Update_" + todayString))

		print("...done making directory for logs!\n ")


	else: pass



# Variable for the file path where all logs and other files will be stored for this maintenance period
currentFolderPath = SDE_maintenance_folderPath + "/Update_" + todayString

print("Assigning variables for log file names...")

# Maintenance Summary Log file name:
maintenance_log_FileName = currentFolderPath + "//Maintenance_Log.txt"

error_Log_FileName = currentFolderPath + "//Error_Log.txt"

# Reconcile & Post Log file name
reconcileFileName = currentFolderPath + "//Reconcile_Log.txt"

print("...done assigning variables for log file names!\n ")

################################################################################################################################
