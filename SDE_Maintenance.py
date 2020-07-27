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


# ================================================================================================================================

##################################################################################################################################

#                                                         BEGIN SCRIPT:

print("Staring script...\n....\n ")

##################################################################################################################################

#                                                        IMPORT MODULES:

print("Importing modules...")

import datetime
import time

from SDE_Maintenance_DateTimeHandling.py import CustomDateTime


script_start_time = None
script_ended_time = None
script_fails_time = None
tz = None

try:

     # Necessary: to get the current date for creating files/logs/directories/etc
    import pytz     # Necessary: to populate the time component of the datetime variable with correct timezone info, default == UTC-0

    tz = pytz.timezone('America/New_York')
    script_start_time = datetime.datetime.now(tz=tz) # date/time script started (will be a few ms behind, b/c of module imports)

    import arcpy    # Essential: to run any of the esri functions/methods called within this script
    import os       # Necessary: to run any of the file I/O methods && for creating a new directory for the Logs

    from subprocess import Popen # Necessary: to run the method call to run external batch files

    print("...module imports complete!\n ")

except ImportError as e:
    print(e)
    error_count = 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Errors.txt", 'a+') as error_Log:
        error_Log.write("\n======================================\n \nError encountered during module import.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    time.sleep(5)
    SystemExit(1)

#################################################################################################################################
#*******************************************************************************************************************************

#Error handling:

def addToErrorLog(error, ErrorDateTime, sectionName):
    print(error)
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Errors.txt", 'a+') as error_Log:
        error_Log.write("\n======================================\n \nError encountered during "+ sectionName + ".\nDetails:\n" + str(error) + '\nError occured at: ' + str(ErrorDateTime) + '\n======================================\n')
        error_Log.close()

#*******************************************************************************************************************************
#################################################################################################################################

#                                            DEFINE FILEPATH/CONNECTION VARIABLES:
#                                    database/server/filepaths removed for security reasons

print("Defining SDE Connection File...")

# define workspace environment file path for the arcpy module
arcpy.env.workspace = r'C:\SDEConnections'

# connection path for the database, change this variable to perform maintenance on a different database
# current path is for the 'REDACTED' instance, 'REDACTED' database

db = ''

try:
    db = r'C:\SDEConnections\SDEADMIN_DEFAULT_DBAUTH.sde'

except Exception as e:
    print(e)
    error_count = 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Errors.txt", 'a+') as error_Log:
        error_Log.write("\n======================================\n \nError encountered when defining SDE connection file.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    time.sleep(5)
    SystemExit(1)

print("...done defining SDE Connection File!\n ")

print("Defining FilePath for SDE Maintenance Output files...")

# filepath where a directory will be created for the current maintenance task(s)
SDE_maintenance_folderPath = r'C:\GIS_Scripts\SDE_Maintenance'

print("...done defining FILEPATH variables!\n ")

print("Assigning maintenance variables...")

section_name    = ''
section_success = bool(False)
overall_success = bool(False)
error_count     = 0

def section_success_str(b):
    if(b):
        return "SUCCESS!"
    else: 
        return "failure!"

def overall_success_str(b):
    if(b):
        return "SUCCESS!"
    else: 
        return "failure!"

print("...done assigning maintenance variables!\n ")

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
# Variable to concatenate the String versions of the "day" "month" and "year" variable into the folowing format: YYYY-MM-DD
todayString = yearString + "-" + monthString + "-" + dayString

print("....done assigning date/time variables!\n ")

################################################################################################################################

#                                    DEFINE VARIABLES THAT ARE DEPENDENT ON THE DATE FUNCTIONS:

print("Making directory for logs...")

os.mkdir(os.path.join(SDE_maintenance_folderPath, "Update_" + todayString))

a = os.path.join(SDE_maintenance_folderPath, "Update_" + todayString)

b = os.direxists(os.path.join(SDE_maintenance_folderPath, "Update_" + todayString))

print("...done making directory for logs!\n ")

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

#                                                MAINTENANCE & ERROR LOG CREATION:

print("Creating 'Maintenance Log' file...")

#Create file for maintenance summary:
maintenance_log = open(maintenance_log_FileName, 'w+')

print("...'Maintenance Log' file created!\n ")


print("Writing template text to 'Maintenance Log' file...")

script_start_time_str_t = str(script_start_time.time())
script_start_time_str_d = str(script_start_time.date())

maintenance_start_time = '\nSDE Maintenance started: ' + script_start_time_str_t + ' on: ' + script_start_time_str_d + ' \n '

# Boiler plate text to add to top of maintenance_summary file
boilerPlate_maintenance = '********************SDE MAINTENANCE LOG:********************\n ' + maintenance_start_time

boilerPlate_maintenance = boilerPlate_maintenance.__add__("""
Maintenance  Activities:\n 
Import relevant modules: SUCCESS!
Assign script variables: SUCCESS!
Create output directory: SUCCESS!
Define fileNames 4 logs: SUCCESS!""")

#write boiler plate to maintenance_summary file
maintenance_log.write(boilerPlate_maintenance)

print("...done writing template text to 'Maintenance Summary' file!\n ")

#close the file
maintenance_log.close()

print("Creating 'Error Log' file...")

#Create file for Error_Log:
error_Log = open(error_Log_FileName, 'w+')

print("...'Error Log' file created!\n ")


print("Writing template text to 'Error Log' file...")

# Boiler plate text to add to top of Error_Log file
boilerPlate_error = '********************ERROR LOG:********************\n \nErrors:'

#write boiler plate to Error_Log file
error_Log.write(boilerPlate_error)

print("...done writing template text to 'Error Log' file!\n ")

#close the file
error_Log.close()

################################################################################################################################

#                                                     PRE-MAINTENANCE CHECKS:

print("Getting list of connected users...")

# method to return a tuple of all currently connected DB users; tuple is assigned to the "userList" variable

userList = []

try:
    userList = arcpy.ListUsers(db) # "db" variable defined in line *31* above

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nGet connectedUsers list: SUCCESS!')
        maintenance_log.close()

    print("...done getting list of connected users!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" +error_count+ "\nError encountered when getting SDE user list.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nGet connectedUsers list: failure!')
        maintenance_log.close()
    pass


print("Writing list of users to .txt file...")


UserList_File = None

try:
    # creates a file object for file I/O, with the name: "UserList_beforeEditSession.txt" within the 
    # current maintenance period folder.  File is opened in write ('w') mode
    UserList_File = open(os.path.join(currentFolderPath, "UserList_beforeEditSession.txt"), 'w')

    # loop to iterate over each item in the 'userList" tuple
    for i in userList:
     # take each item in the tuple, cast it to a String, then write it to the .txt file object created in the previous step
	UserList_File.write(''.join(str(s) for s in i) + '\n')

    # method to close the file which saves the file and also prevents the file object from persisting in system memory
    UserList_File.close()

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nWrite user list to file: SUCCESS!')
        maintenance_log.close()

    print("...done writing list of users to .txt file!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered when writing SDE user list to .txt file.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nWrite user list to file: failure!')
        maintenance_log.close()
    pass

print("Blocking new connections to database...")

try:
    # method to prevent any additional connections to the DB
    arcpy.AcceptConnections(db, False)

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nStop any new connection: SUCCESS!')
        maintenance_log.close()

    print("...done blocking new connections to database!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered when blocking new connections to sde.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nStop any new connection: failure!')
        maintenance_log.close()
    pass

print("Wating 1 minute to allow time for currently connected users to save and log off...")

try:
    # optional method to wait 15 minutes after blocking all new connections
    # this method can be used if you want to send out notifications to users that are still connected to save, log-off, etc.
    time.sleep(60) 

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nWait for userDisconnect: SUCCESS!')
        maintenance_log.close()

    print("...done wating 1 minute")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered while waiting for users to disconnect.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nWait for userDisconnect: failure!')
        maintenance_log.close()
    pass

################################################################################################################################

#                                        ACTUAL DATABASE MAINTENANCE ACTIVITY BEGINS HERE:


################################################################################################################################

#                                                       DISCONNECT USERS:

print("Booting all users...")

try:

    # method to disconnect all SDE users
    arcpy.DisconnectUser(db, 'ALL')

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nBoot all connectedUsers: SUCCESS!')
        maintenance_log.close()

    print("...all users Booted!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered attempting to disconnect all users.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nBoot all connectedUsers: failure!')
        maintenance_log.close()
    pass

print("Printing list of all users to confirm all are disconnected...\n ")

# optional method to list all db users again after the DisconnectUser method (to make sure all users were indeed disconnected)
userList1 = arcpy.ListUsers(db)

#prints the above "userList1" variable to the system console
print(userList1)

################################################################################################################################

#                            METHOD TO CALL THE BATCH SCRIPT TO STOP THE SERVICE FOR ARCGIS SERVER:

print("\nStopping the 'ArcGIS Server' service...")

try:
    p = Popen("C:\\BatchFiles\\Stop_ArcGIS_Server.bat")
    stdout, stderr = p.communicate()

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nStop ArcGISsrvr service: SUCCESS!')
        maintenance_log.close()    

    print("...'ArcGIS Server' service stopped!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered attempting to stop the 'ArcGIS Server' service.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nStop ArcGISsrvr service: failure!')
        maintenance_log.close()
    pass


################################################################################################################################

#                                                   LOG CURRENT DB VERSIONS:

print("Getting list of database versions...")


# gets a tuple of all current DB versions and assigns the tuple to the "versionList" variable
versionList = arcpy.ListVersions(db)

print("...done getting list of versions!\n ")

print("Writing list of versions to .txt file...")

# creates a file object for file I/O, with the name: "VersionList_beforeEditSession.txt" within the 
#  current maintenance period folder.  File is opened in write ('w') mode
file = open(os.path.join(currentFolderPath, "VersionList_beforeEditSession.txt"), 'w')

# loop to iterate over each item in the 'VersionList" tuple
for i in versionList:
     # take each item in the tuple, cast it to a String, then write it to the .txt file defined created in the previous step
	file.write(''.join(str(s) for s in i) + '\n')

    # method to close the file which saves the file and also prevents the file object from persisting in system memory
file.close()

print("...done writing list of versions to .txt file!\n ")

#################################################################################################################################

#                                                   RECONCILE & POST VERSIONS:

print("Reconciling, Posting, && Deleting versions....")

# method to Reconcile && Post && Delete all child versions up to DEFAULT
arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", "dbo.DEFAULT", versionList, "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION","POST", 
                                   "DELETE_VERSION", reconcileFileName)

# NOTE: this method will also DELETE all child versions

print("...ALL VERSIONS RECONCILED, POSTED & ALL CHILD VERSIONS DELETED!!\n ")

################################################################################################################################

#                                                         DB COMPRESS:

print("Compressing database....")

# Run the compress tool. 
arcpy.Compress_management(db)

print("....Database compress complete!\n ")

print("Rebuilding indexes....")

# Rebuild indexes and analyze the states and states_lineages system tables
arcpy.RebuildIndexes_management(db, "SYSTEM", "", "ALL")

print("....done rebuilding indexes!\n ")

################################################################################################################################

#                                                   ANALYZE  SYSTEM  TABLES:

print("Analyzing database....")

# method to analyze the states and states_lineages system tables
arcpy.AnalyzeDatasets_management(db, "SYSTEM", "", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")

print("....analysis complete!\n ")

################################################################################################################################                       

#                                          ALLOW NEW CONNECTIONS TO THE DATABASE:

print("Re-allowing database connections....")

arcpy.AcceptConnections(db, True)

print("...database now accepting new connections!\n ")


################################################################################################################################

#                          METHOD TO CALL THE BATCH SCRIPT TO RESTART THE SERVICE FOR ARCGIS SERVER:

print("\nRestarting the 'ArcGIS Server' service...")

try:
    p = Popen("C:\\BatchFiles\\Start_ArcGIS_Server.bat")
    stdout, stderr = p.communicate()
    
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nRestart ArcServ service: SUCCESS!')
        maintenance_log.close()

    print("...'ArcGIS Server' service Started!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered attempting to RESTART the 'ArcGIS Server' service.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nRestart ArcServ service: failure!')
        maintenance_log.close()
    pass

################################################################################################################################ 

#                                               RE-CREATE ALL USER VERSIONS:

print("Re-creating database versions....")

# Set local variables
parentVersion    = "dbo.QC"
versionName      = "QC"
accessPermission = "PROTECTED"

print("....\n ")


try:
    # creates a QC version w/ parent version= 'DEFAULT'  # all user versions have parent version= 'QC'
    arcpy.CreateVersion_management(db, "dbo.DEFAULT", versionName, "PUBLIC")

    # loop to iterate over each user in the userList tuple & recreate that version
    for version in versionList:  # "versionList" variable defined in line *161* above
	
	    # if statement to find all named (user) versions
        if(version != "dbo.DEFAULT" and version != "DBO.QC"):
            if("DBO." in version or "dbo." in version):
                versionName = version[4:]
                arcpy.CreateVersion_management(db, parentVersion, versionName, accessPermission)
            else: 
                versionName = version
                arcpy.CreateVersion_management(db, parentVersion, versionName, accessPermission)
        else: 
            continue # this will skip over the "dbo.DEFAULT" & "DBO.QC" items in the versionList tuple

    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nRe-create  all versions: SUCCESS!')
        maintenance_log.close()
    
    print("ALL VERSIONS RECREATED!!!\n ")

except Exception as e:
    print(e)
    error_count = error_count + 1
    script_fails_time = datetime.datetime.now()
    with open("C:\\GIS_Scripts\\SDE_Maintenance\\Update_2018-08-14\\Error_Log.txt", 'a+') as error_Log:
        error_Log.write("\n" + str(error_count) + "\nError encountered attempting to recreate versions.\nDetails:\n" + str(e) + '\nError occured at: ' + str(script_fails_time) + '\n======================================\n')
        error_Log.close()
    with open(maintenance_log_FileName, 'a+') as maintenance_Log:
        maintenance_Log.write('\nRe-create  all versions: failure!')
        maintenance_log.close()
    

################################################################################################################################

#                                         LOG DB VERSIONS AFTER DB MAINTENANCE:

print("Getting list of new versions...")

# list all current versions, assigne to new "versionList2" varaiable
versionList2 = arcpy.ListVersions(db)

print("...done getting list of versions!\n ")


print("Writing list of versions to .txt file...")

# creates a file object for file I/O, with the name: "VersionList_AfterEditSession.txt" within the 
#  current maintenance period folder.  File is opened in write ('w') mode
file = open(os.path.join(currentFolderPath, "VersionList_AfterEditSession.txt"), 'w')

# loop to iterate over each item in the 'VersionList2" tuple
for i in versionList2:
     # take each item in the tuple, cast it to a String, then write it to the .txt file defined created in the previous step
    file.write(''.join(str(s) for s in i) + '\n')

# method to close the file which saves the file and also prevents the file object from persisting in system memory
file.close()

print("...new versions logged in .txt file!\n ")

if(error_count == 0):
    with open(error_Log_FileName, 'a') as error_Log:
        error_Log.write("\n\nMaintenance completed without errors!")
        error_Log.close()
else:
    with open(error_Log_FileName, 'a') as error_Log:
        error_Log.write("\n\nUh-oh! Something went wrong :-(")
        error_Log.close()

print("\nMAINTENANCE COMPLETE!")

################################################################################################################################
#                                                                                                                              #
#                                                     *** THE END ***                                                          #
#                                                                                                                              #
################################################################################################################################


#================================================================================================================================


################################################################################################################################
#                                                                                                                              #
#                                                 * STILL NEED TO ADD: *                                                       #
#                                                                                                                              #
#    > Exception handling (try, except --> write to errorLog.txt file for any errors)                                          #
#                                                                                                                              #
#                                                                                                                              #
################################################################################################################################
