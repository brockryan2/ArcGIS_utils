import os
from datetime import datetime
from CustomDateTime import CustomDateTime

class LogFile(object):

    name = ''
    file_path = ''
    boiler_plate = ''

    template = {
        'folder':             0,
        'maintenance':        1,
        'error':              2,
        'reconcile':          3,
        'user_before':        4,
        'version_before':     5,
        'user_after':         6,
        'version_after':      7,
    }

    global log_type
    log_type = -1

    global log
    log = CustomDateTime(datetime.now())

    global boiler_plate_maintenance
    boiler_plate_maintenance = "********************SDE MAINTENANCE LOG:********************\n \n" + "SDE Maintenance began at: " + log.time + " on: " + log.date + "\n \nMaintenance Activities:\n "

    global boiler_plate_error
    boiler_plate_error = '********************ERROR LOG:********************\n \nErrors:'


    def __init__(self, log_type, file_path, *args, **kwargs):
            return super().__init__(*args, **kwargs)

            self.file_path = file_path
            self.log_type  = LogFile.template[log_type]
            self.log = CustomDateTime(datetime.now())

            if(self.log_type == 0):
                self.name = 'Update_' + self.log.date
            
            elif(self.log_type == 1):
                self.name         = '//Maintenance_Log.txt'
                self.boiler_plate = boiler_plate_maintenance

            elif(self.log_type == 2):
                self.name         = '//Error_Log.txt'
                self.boiler_plate = boiler_plate_error

            elif(self.log_type == 3):
                self.name         = "//Reconcile_Log.txt"

            elif(self.log_type == 4):
                self.name         = "//User_Log_beforeMaintenance.txt"

            elif(self.log_type == 5):
                self.name         = "//Version_Log_beforeMaintenance.txt"

            elif(self.log_type == 6):
                self.name         = "//User_Log_afterMaintenance.txt"

            elif(self.log_type == 7):
                self.name         = "//Version_Log_afterMaintenance.txt"

            else: pass


    def createDirectory(self):
        if(self.log_type == 0):
            try:
                if(os.path.isdir(os.path.join(self.file_path, self.name))):
                    pass
                else:
                    os.mkdir(os.path.join(self.file_path, self.name))
            
            except Exception as e:
                print(e)
        else: pass

    def createFile(self):
        try:
            absolute_path = self.file_path + self.name
            file = open(absolute_path, 'w+')
            file.close()

        except Exception as e:
            print(e)
            pass
    
    def appendToFile(self, text_tuple):

        for item in text_tuple:
            try:
                absolute_path = self.file_path + self.name

                with open(absolute_path, 'a+') as log:
                    log.write(item)
                    log.close()
        
            except Exception as e:
                print(e)
                pass


# make directory/folder(file_path, dir_name)

# create file(file_name, file_path)

# write boiler plate to file(text to write, fileName/path)

# append to file

# close file


#			create()
#			write(boiler_plate)
#			append(file_path, 'a+', maintenance_item[#], maintenance_item_status['s'/'f'])
#			close()
#
#		error log
#			file_name = "//Error_Log.txt"
#			file path = folderPath + file_name
#
#		reconcile log ------ created by ArcGIS, so no need for creating a file object for this, just need a file path & file_name
#		user list - before
#		user list - after
#		version list - before
#		version list - after

maintenance_item = {
                1:  '\nImport all relevant modules: ',
				2:  '\nAssign necessary  variables: ',
				3:  '\nCreate  output  directories: ',
				4:  '\nDefine file names for  logs: ',
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

status = ('failure!', 'SUCCESS!')


