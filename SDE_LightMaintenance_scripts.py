## Individual Reconcile & Post Scripts
#=========================================================================================================================================================
# BRyan to QC
import arcpy
import datetime

db = r'X:\\GIS\\GIS\\ReferenceDocs\\SDEMaintenance\\Pro_ProjectFolder\\cc-gis-sql.sde'

versionList   = arcpy.ListVersions(db)
parentVersion = 'DBO.QC'
versionName   = 'DBO.BRyan'

today = datetime.datetime.now()
todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "_" + str(today.hour) + str(today.minute) + str(int(today.second))

currentFolderPath = r'X:\GIS\GIS\ReferenceDocs\SDEMaintenance\Individual_Rec_and_Post_Logs' 
reconcileFileName = currentFolderPath + "//" + todayString + "_Rec_Post.txt"

arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", parentVersion, versionName, "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_EDIT_VERSION","POST", 
                                   "KEEP_VERSION", reconcileFileName)

#=========================================================================================================================================================
# QC to DEFAULT
import arcpy
import datetime

db = r'X:\\GIS\\GIS\\ReferenceDocs\\SDEMaintenance\\Pro_ProjectFolder\\cc-gis-sql.sde'

parentVersion = 'dbo.DEFAULT'
versionName = "DBO.QC"

today = datetime.datetime.now()
todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "_" + str(today.hour) + str(today.minute) + str(int(today.second))

currentFolderPath = r'X:\GIS\GIS\ReferenceDocs\SDEMaintenance\Individual_Rec_and_Post_Logs'
reconcileFileName = currentFolderPath + "//" + todayString + "_Rec_Post.txt"

arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", parentVersion, versionName, "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_EDIT_VERSION","POST", 
                                   "KEEP_VERSION", reconcileFileName)

#==========================================================================================================================================================
## Reconcile all child versions of QC up to QC, then QC up to DEFAULT
import arcpy
import datetime

db = r'X:\\GIS\\GIS\\ReferenceDocs\\SDEMaintenance\\Pro_ProjectFolder\\cc-gis-sql.sde'

versionList   = arcpy.ListVersions(db)
parentVersion = 'DBO.QC'

childrenOfQC = []

numList = 


for i in numList:
    version = versionList[i]
    if("DEFAULT" in version or "QC" in version):
        pass
    else: childrenOfQC.append(version)


for version in childrenOfQC:
    today = datetime.datetime.now()
    todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "_" + str(today.hour) + str(today.minute) + str(int(today.second))

    reconcileFileName = r'X:\GIS\GIS\ReferenceDocs\SDEMaintenance\Individual_Rec_and_Post_Logs' + "//" + todayString + "_Rec_Post.txt"

    arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", parentVersion, version, "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_EDIT_VERSION","POST", 
                                   "KEEP_VERSION", reconcileFileName)

today = datetime.datetime.now()
todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "_" + str(today.hour) + str(today.minute) + str(int(today.second))

arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", 'dbo.DEFAULT', 'DBO.QC', "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_EDIT_VERSION","POST", 
                                   "KEEP_VERSION", reconcileFileName)



#==========================================================================================================================================================

#Rec & POST Mesha's version up to DEFAULT:

import arcpy
import datetime

db = r'X:\\GIS\\GIS\\ReferenceDocs\\SDEMaintenance\\Pro_ProjectFolder\\cc-gis-sql.sde'

  #Mesha's version up to QC:

today = datetime.datetime.now()
todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "_" + str(today.hour) + str(today.minute) + str(int(today.second))

reconcileFileName = r'X:\GIS\GIS\ReferenceDocs\SDEMaintenance\Individual_Rec_and_Post_Logs' + "//" + todayString + "_Rec_Post.txt"

arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", 'DBO.QC', '"SANDYSPRINGS\\MESHA.CISERO".MCisero', "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_EDIT_VERSION","POST", 
                                   "KEEP_VERSION", reconcileFileName)

  # QC up to DEFAULT

today = datetime.datetime.now()
todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "_" + str(today.hour) + str(today.minute) + str(int(today.second))

reconcileFileName = r'X:\GIS\GIS\ReferenceDocs\SDEMaintenance\Individual_Rec_and_Post_Logs' + "//" + todayString + "_Rec_Post.txt"

arcpy.ReconcileVersions_management(db, "ALL_VERSIONS", 'dbo.DEFAULT', 'DBO.QC', "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_EDIT_VERSION","POST", 
                                   "KEEP_VERSION", reconcileFileName)






# import modules
import os
import arcpy
import System
import getpass

# define initial variables, empty variables declared here to initialize them in global scope so they can be used within different local-scoped blocks
database_connection_file     = ""
database_parent_version      = "dbo.QC"

# this part of the database user version name is common to all users who connect to the EGDB according to
#   the criteria listed in the ReadMe.txt file located here: X:\Shared Between Depts\GIS\SDE_Version_Management
database_user_version_prefix = r'"SANDYSPRINGS\"'

database_user_version_suffix = ""
database_user_version_full   = ""
Operating_system_username    = ""
username_firstName_initial   = ""
username_lastName_full       = ""
db_version_access_permission = "PROTECTED"  # current policy = we want all user versions to have a db version access permission of 'protected.' Change this variable if this policy ever changes.


try:
	# attempt to overwrite the blank OS username variable by using the python getpass module to access the currently logged-in user's username from their local machine (may require admin permission)
	Operating_system_username = getpass.getuser()

except Exception as e:
	print("an error occurred attempting to automatically identify the user's OS username. Terminating program....")
    # insert snippet to write any errors to a log file here
	System.exit(1)


try:
	# file path to the user's .sde connection file created by ArcGIS Desktop / Pro when they initially connected to the EGDB manually
    database_connection_file = r'REPLACE THIS TEXT WITH YOUR SDE CONNECTION PATH'

except Exception as e:
    print("Unable to connect to database with connection file specified.\nPlease check that you have the correct UNC path to the appropraite .sde connection file and try again.\n")
    # insert snippet to write any errors to a log file here
    System.exit(1)


try:
	# get OS username from user's machine, get first letter of first name portion of username
    username_firstName_initial = str(Operating_system_username[:1])
    # temporary place holder variable to split the components of the user's OS username into first name and last name (splits on the '.' portion of the username)
    temp_variable              = Operating_system_username.split('.')
    # assign last name portion of user's OS username to the username_lastName_full variable
    username_lastName_full     = str(temp[1])
    
    # change the user's first name initial portion of their username to UPPERCASE
    username_firstName_initial = username_firstName_initial.upper()
    # change the user's last name portion of their username to UPPERCASE
    username_lastName_full = username_lastName_full.upper()

    # get user's full OS username and convert to all UPPERCASE
    Operating_system_username = str(Operating_system_username).upper()

    # populate the suffix portion of the database user version from the above OS username components
    database_user_version_suffix = Operating_system_username + '".' + username_firstName_initial + username_lastName_full

    # populate the final database user version by concatenating the prefix defined at the beginning of the script with the suffix defined in the previous step
    database_user_version_full = database_user_version_prefix + database_user_version_suffix


except Exception as e:
	print("an error occurred attempting to create the user's database user version name from the user's OS username. Terminating program....")
    # insert snippet to write any errors to a log file here
    # insert optional logic to look for the users database version name in an alternate location - if so, do not terminate the program
	System.exit(1)


parent_version = "dbo.QC"
version = r'"SANDYSPRINGS\MESHA.CISERO".MCisero'

arcpy.CreateVersion_management(db, database_parent_version, database_user_version, db_version_access_permission)
