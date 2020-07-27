import arcpy
import CustomDateTime
import LogFile
import datetime
import os
import urllib


#def main():
#
#    file_path, sde_workspace, sde_connection, time_delay, batchFile_stop, #batchFile_start, email_server, email_domain, email_from = **args
#    
#    maintenance_session = SDEmaintenance(file_path, sde_workspace, #sde_connection, time_delay, batchFile_stop, batchFile_start)
#
#    maintenance_session.setupWorkEnv()
#
#    email = maintenance_session.setEmailParameters()
#
#    maintenance_session.getUsers()
#
#    maintenance_session.preventNewConnections()
#
#    maintenance_session.sendEmail(email)
#
#    maintenance_session.bootUsers()
#
#    maintenance_session.stopServices()
#
#    maintenance_session.getVersions(1)
#
#    maintenance_session.reconcile()
#
#    maintenance_session.compress()
#
#    maintenance_session.rebuildIndexes()
#
#    maintenance_session.analyze()
#
#    maintenance_session.acceptNewConnections()
#
#    maintenance_session.startServices()
#
#    maintenance_session.recreateVersions()
#
#    maintenance_session.getVersions(2)
#
#main()
