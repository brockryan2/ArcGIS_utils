import CustomDateTime
import datetime
import os
import smtplib
import time
import arcpy
import LogFile as logFile
from subprocess import popen

class SDEmaintenance(object):

    def timeDelayCheck(t):
        if(t > 0 and t <= 1800):
            time_delay = t
        elif(t > 1800):
            time_delay = 1800
        else:
            time_delay = 0

        return time_delay

    def __init__(self, file_path, sde_workspace, sde_connection, time_delay, batchFile_stop, batchFile_start, email_server, email_domain, email_from, *args, **kwargs):
        return super().__init__(*args, **kwargs)
        self.startTime = datetime.datetime.now()
        self.file_path = file_path
        self.sde_workspace = sde_workspace
        self.sde_connection = sde_connection
        self.time_delay = self.timeDelayCheck(time_delay)
        self.maintenance_item = {
            1:  '\nImport all relevant modules: ',
			2:  '\nAssign maintnance variables: ',
			3:  '\nCreate directory for output: ',
			4:  '\nCreate necessary  log files: ',
			5:  '\nGet list of connected users: ',
			6:  '\nWrite user list to log file: ',
			7:  '\nPrevent any new connections: ',
			8:  '\nWait for users toDisconnect: ',
			9:  '\nDisconnect all active users: ',
			10: '\nStop ArcGIS Server  service: ',
			11: '\nGet list of all DB versions: ',
			12: '\nRec,Post & Del all versions: ',
			13: '\nCompress database A&Dtables: ',
			14: '\nAnalyze & update statistics: ',
			15: '\nRe-allow new DB connections: ',
			16: '\nRe-start GIS Server service: ',
			17: '\nRe-create database versions: ',
			18: '\nLog versions after maintnce: ',
			19: '\n\nOverall maintenance results: '
		}

        self.errorTemplate_text = {
            1: '\nError encountered while ',
            2: '\nDetails:\n ',
            3: '\nError occured at: ',
            4: '\n======================================\n',
        }

        self.item_message = {
            0:  '',
            1:  'importing modules. ',
			2:  'assigning maintenance  variables. ',
			3:  'creating  directory for maintenance outputs/logs. ',
			4:  'creating log files. ',
			5:  'getting a list of all connected users. ',
			6:  'writing user list to user-log file. ',
			7:  'attempting to prevent new connections to the database. ',
			8:  'waiting ' + time_delay + 'seconds for users to disconnect. ',
			9:  'disconnecting all active users. ',
			10: 'stopping the ArcGIS Server service. ',
			11: 'getting a list of all DB versions. ',
			12: 'reconciling, posting & deleting versions. ',
			13: 'compressing database tables. ',
			14: 'analyzing & updating database statistics. ',
			15: 're-allowing new database connections. ',
			16: 're-starting the ArcGIS Server service. ',
			17: 're-creating database versions (owned by .dbo). ',
			18: 'logging versions after maintenance. ',
			19: 'doing some other task. '
        }

        self.batchFile_stop  = batchFile_stop
        self.batchFile_start = batchFile_start

        self.email_server = email_server
        self.email_domain = email_domain
        self.email_from   = email_from
        self.email_message= f"Auto generated Message.\n\rServer maintenance will be performed in {self.time_delay/60} minutes. Please log off."

        self.versionList = []

        self.reconcile_log = file_path + "//Reconcile_Log.txt"

        self.current_item = 1

        self.part = 1

        self.maintenance_status = ('failure!', 'SUCCESS!')

        self.error_count = 0

    def itemPrint(self):
        if(self.part == 1):
            print(self.item_message[self.current_item] + " ...")
            self.part += 1

        elif(self.part == 2):
            print("... done " + self.item_message[self.current_item] + "!")
            self.part = 1
        
        else:
            print("something went wrong :-(")

    def handleException(self, exception):
        print(exception)

        self.error_count += 1 
        error_dateTime = CustomDateTime(datetime.datetime.now())

        maintenance_Log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[0]])

        error_log.appendToFile([self.error_count, self.errorTemplate_text[1], self.item_message[self.current_item], self.errorTemplate_text[2], str(exception), self.errorTemplate_text[3], error_dateTime.time, " on ", error_dateTime.date, self.errorTemplate_text[4]])
    
    def defineArcpyWorkspace(self):
        return self.sde_workspace

    def defineDBconnection(self):
        return self.sde_connection

    def setEmailParameters(self):
        smtplib_object = smtplib.SMTP(self.email_server)
        return smtplib_object

    def generateEmailList(self, versionList):
        emailList = []

        for item in versionList:
            #do some string parsing / processing of item & assign item to new var
            email_item = item[:4]
            emailList.append(email_item)

            return emailList
            
    def sendEmail(self, smtp_object):
        email = smtp_object
        v_L = self.getVersions

        if(self.time_delay > 300):
            smtp_object.sendmail(self.email_from, self.generateEmailList(v_L), self.email_message)
        else: print("\nThe time delay interval is too short to give users enough time to save their work and log off.  Email is not being sent.\n")
        
    def setupWorkEnv(self):
        self.current_item += 2

        self.itemPrint() # ↓
        workspace = self.sde_workspace
        arcpy.env.workspace = workspace

        global folder
        global maintenance_log
        global error_log
        global reconcile_log
        global user_before_log
        global version_before_log
        global user_after_log
        global version_after_log

        folder = logFile('folder', self.file_path)
        folder.createDirectory()
        self.itemPrint() # ↑

        self.current_item += 1

        self.itemPrint() # ↓
        maintenance_log    = logFile('maintenance', self.file_path)
        error_log          = logFile('error', self.file_path)
        reconcile_log      = logFile('reconcile', self.file_path)
        user_before_log    = logFile('user_before', self.file_path)
        version_before_log = logFile('version_before', self.file_path)
        user_after_log     = logFile('user_after', self.file_path)
        version_after_log  = logFile('version_after', self.file_path)

        error_log.createFile()
        reconcile_log.createFile()
        user_before_log.createFile()
        version_before_log.createFile()
        user_after_log.createFile()
        version_after_log.createFile()
        self.itemPrint() # ↑

        # return workspace

      # maintenance_log.appendToFile([]) this part needs more work/logic. e.g. only write "success" if activity is actually successful

    def getUsers(self):
        self.current_item += 1

        global userList

        self.itemPrint() # ↓
        try:
            userList = arcpy.ListUsers(self.sde_connection)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)


        self.current_item += 1


        self.itemPrint() # ↓
        try:
            user_before_log.appendToFile(userList)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def preventNewConnections(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            arcpy.AcceptConnections(self.sde_connection, False)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])
        
        except Exception as e:
            self.handleException(e)

    def bootUsers(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            time.sleep(self.time_delay)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1] + "   wait time: " + self.time_delay])

        except Exception as e:
            self.handleException(e)


        self.current_item += 1


        self.itemPrint() # ↓
        try:
            arcpy.DisconnectUser(self.sde_connection, 'ALL')
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def stopServices(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            p = popen(self.batchFile_stop)
            stdout, stderr = p.communicate()
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])
        
        except Exception as e:
            self.handleException(e)

    def getVersions(self, order):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            self.versionList = arcpy.ListVersions(self.sde_connection)
            versionList = self.versionList

            if(order == 1):
                version_before_log.appendToFile(versionList)

            elif(order == 2):
                version_after_log.appendToFile(versionList)

            else: version_log = logFile('version', self.file_path)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

            return versionList

        except Exception as e:
            self.handleException(e)

    def reconcile(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            arcpy.ReconcileVersions_management(self.sde_connection, "ALL_VERSIONS", "dbo.DEFAULT", self.versionList, "LOCK_ACQUIRED", 
                                   "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION","POST", 
                                   "DELETE_VERSION", self.reconcile_log)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def compress(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            arcpy.Compress_management(self.sde_connection)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def rebuildIndexes(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            arcpy.RebuildIndexes_management(self.sde_connection, "SYSTEM", "", "ALL")
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def analyze(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            arcpy.AnalyzeDatasets_management(self.sde_connection, "SYSTEM", "", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def acceptNewConnections(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            arcpy.AcceptConnections(self.sde_connection, True)
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])
        
        except Exception as e:
            self.handleException(e)

    def startServices(self):
        self.current_item += 1

        self.itemPrint() # ↓
        try:
            p = popen(self.batchFile_start)
            stdout, stderr = p.communicate()
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])
        
        except Exception as e:
            self.handleException(e)

    def recreateVersions(self):
        self.current_item += 1

        version_name      = "QC"
        parent_version    = "dbo.QC"
        access_permission = "PROTECTED"

        self.itemPrint() # ↓
        try:
            arcpy.CreateVersion_management(self.sde_connection, "dbo.DEFAULT", version_name, "PUBLIC")

            for version in self.versionList:
                if(version != "dbo.DEFAULT" and version != "DBO.QC"):
                    if("DBO." in version or "dbo." in version):
                        version_name = version[4:]
                        arcpy.CreateVersion_management(self.sde_connection, parent_version, version_name, access_permission)
                    else: 
                        versionName = version
                        arcpy.CreateVersion_management(self.sde_connection, parent_version, version_name, access_permission)
                else: 
                    continue
            self.itemPrint() # ↑

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1]])

        except Exception as e:
            self.handleException(e)

    def endMaintenance(self):
        self.current_item += 1
        now = datetime.datetime.now()
        
        global maintenance_end
        
        maintenance_end = CustomDateTime(now)
        elapsed_time = now - self.startTime

        if(self.error_count <= 0):

            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[1],
                                     "!!\n \nMaintenance ended successfully at: ", maintenance_end.time, " on ",
                                     maintenance_end.date, "\n \nElapsed time: ", elapsed_time])

            error_log.appendToFile(["\n\nMaintenance completed successfull with [0] errors!!!"])

        else:
            maintenance_log.appendToFile([self.maintenance_item[self.current_item], self.maintenance_status[0],
                                     " :-(\n \nMaintenance terminated at: ", maintenance_end.time, " on ",
                                     maintenance_end.date, "\n \nElapsed time: ", elapsed_time])

            error_log.appendToFile(["\n\n\n \nMaintenance terminated at: ", maintenance_end.time, " on ",
                                     maintenance_end.date, "Number of errors recorded: [", self.error_count, "]"])

        print("Maintenance complete!!\nNumber of errors: " + self.error_count + "\nElapsed time: " + elapsed_time)
