print("importing libraries...")

import arcpy
import urllib.request
from http.client import responses
from datetime import datetime
from CustomDateTime import CustomDateTime

system_start_datetime = datetime.now()

start_datetime = CustomDateTime(system_start_datetime)
date = start_datetime.date

tm = system_start_datetime.time()
temp = str(tm)
temp = temp.split(".")
temp = temp[0]
temp_split = temp.split(":")
time_string = ""

for item in temp_split:
    time_string = time_string + str(item)

time = time_string

print("defining workspace...")
arcpy.env.workspace = "X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase"

db = r'X:\GIS\Addressing\Address_Review_Pro\COSS_Vector--BRyan.sde'

print("defining tables...")

tables = ("X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase\\sde_COSS_vector.DBO.FC_GeoPlat_Area",
"X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase\\sde_COSS_vector.DBO.FC_Modifications",
"X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase\\sde_COSS_vector.DBO.FC_Use",
"X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase\\sde_COSS_vector.DBO.FC_Variances",
"X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase\\sde_COSS_vector.DBO.FC_Zoning_Case",
"X:\\GIS\\Addressing\\Address_Review_Pro\\COSS_Vector--BRyan.sde\\sde_COSS_vector.DBO.LandBase\\sde_COSS_vector.DBO.GeoPlat_Area")

tableDictionary = {tables[0]: "Fulton County GeoPlats", tables[1]: "Fulton County Modifications", tables[2]: "Fulton County Use Permits", tables[3]: "Fulton County Variances", tables[4]: "Fulton County ReZoning", tables[5]: "Sandy Springs GeoPlats"}

print("defining script variables...")

table_name = ""
objectID   = ""
web_link   = ""
httpCode   = 0
codeDescr  = ""

fields = ("OID@", "Web_Link")

table_names_string = ""


print("creating log files...")

for table in tables:
    table_names_string = table_names_string + tableDictionary[table] + "\n"

log_file   = r'X:\GIS\GIS\Python\Hyperlink_testing\link_status_log'
log_file   = log_file + "_" + date + "_" + time + ".txt"
error_file = r'X:\GIS\GIS\Python\Hyperlink_testing\link_errors_log'
error_file = error_file + "_" + date + "_" + time + ".txt"

log = open(log_file, 'w+')

log.write("GIS Web Link Status Report:\n \nTest started at: " + str(system_start_datetime) + "\n \nTables searched: \n" + table_names_string + "\n")

log.close()

eror_log = open(error_file, 'w+')

eror_log.write("GIS Web Link Errors:\nerror number:  Table Name:    Object ID:  HTTP Code:  Link:\n \n")

eror_log.close()

print("defining functions...")

def getHTTPcode(url):
    code = 404
    try:
        urlObject = urllib.request.urlopen(url)
        code = urlObject.getcode()
    except Exception as e:
        print("url error encountered: " + str(code) + "  " + str(e))

    if(type(code) == int):
        return code

    else: return -1


def getHTTPcodeDescription(code):
    if(code >= 0):
        return str(responses[code])
    else: return "Unrecognized http response code"


table_count = 0
total_link_error_count = 0
total_rows = 0

print("beginning loop through tables...")

for table in tables:
    table_name = tableDictionary[table]
    table_count = table_count + 1

    print("starting table " + str(table_count))
    row_count = 0
    link_error_count = 0
    rows = arcpy.da.SearchCursor(table, fields)

    with open(log_file, 'a+') as log:
        log.write("\nTable: " + str(tableDictionary[table]) + "\nObject ID\tLink\t\t\t\t\t\t\t\t\t\tHTTP Code:\tHTTP Code Description:\n")
    log.close()

    with open(error_file, 'a+') as error_log:
        error_log.write("\n \nBegin Table " + str(table_count) + ":\n \n")

    with arcpy.da.SearchCursor(table, ("OID@", "Web_Link")) as rows:
        for row in rows:
            row_count = row_count + 1
            total_rows = total_rows + 1
            OID  = ('{0}'.format(row[0]))
            url  = ('{0}'.format(row[1]))
            code = int(getHTTPcode(url))
            desc = str(getHTTPcodeDescription(code))

            if(code != 200):
                link_error_count = link_error_count + 1
                total_link_error_count = total_link_error_count + 1
                with open(error_file, 'a+') as error_log:
                    error_log.write(str(link_error_count) + " \t " + str(tableDictionary[table]) + " \t " + OID + " \t " + str(code) + " \t " + str(url) + "\n")


            with open(log_file, 'a+') as log:
                log.write(OID + "\t" + url + "\t\t" + str(code) + "\t" + str(desc) + "\n")


            print(OID + "\t" + url + "\t\t" + str(code) + "\t" + str(desc) + "\n")


    print("done searching table " + str(table_count) + "\n" + str(row_count) + " records searched, " + str(link_error_count) + " link errors found.")


    with open(log_file, 'a+') as log:
        log.write("\n" + str(row_count) + " rows searched, " + str(link_error_count) + " link errors found\n------------END TABLE " + str(table_count) + "------------\n \n")
        log.close()

    with open(error_file, 'a+') as error_log:
        error_log.write("\n \n------------END TABLE " + str(table_count) + "------------\n \n" + str(link_error_count) + " link errors found, out of " + str(row_count) + " records.\n")

    print("\n" + str(row_count) + " rows searched from table: " + str(table_name) + ", " + str(link_error_count) + " link errors found.\n")

system_end_datetime = datetime.now()
elapsed_time = system_end_datetime - system_start_datetime

with open(log_file, 'a+') as log:
    log.write("\nTest ended at: " + str(system_end_datetime) + "\nSearched " + str(total_rows) + " records from " + str(table_count) + " tables in " + str(elapsed_time.seconds) + " seconds.\nLink errors found: " + str(total_link_error_count) + "\nPercent link failure rate: " + str(total_link_error_count/total_rows))

print("Test ended at: " + str(system_end_datetime) + "\nSearched " + str(total_rows) + " records from " + str(table_count) + " tables in " + str(elapsed_time.seconds) + " seconds.\nLink errors found: " + str(total_link_error_count) + "\nPercent link failure rate: " + str(total_link_error_count/total_rows))
