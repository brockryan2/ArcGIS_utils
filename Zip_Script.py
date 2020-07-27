# @brock ryan

#directory of shapefiles to zip for zipping individual shapefiles
 
#import modules needed
import os
import glob
from zipfile import *
 
#define location of shapefiles and destination of zipped shapefiles
source = r"X:\GIS\GIS\Projects\2013_AerialandLidarDeliverable\Lidar\Roswell_GA_LiDAR\COSS_LAS"
dest = r"X:\GIS\GIS\Projects\2013_AerialandLidarDeliverable\Lidar\Roswell_GA_LiDAR\COSS_LAS\zip"
 
#change the current directory
os.chdir(source)
 
#test current directory
retval = os.getcwd()
print retval
 
#list all files with extension .las
las = glob.glob(source+"/*.las")
print las
 
# create empty list for zipfile names
ziplist = []
 
# create destination directory if it does not exist
if not os.path.exists(dest):
    os.makedirs(dest)
 
#populate ziplist list of unique shapefile root names by finding all files with .las extension and removing extension
for name in las:
  #prints full path for each shapefile
  print name
  #retrieves just the files name for each name in las
  file = os.path.basename(name)
  #removes .las extension
  names = file[:-4]
  #adds each shapefile name to ziplist list
  ziplist.append(names)
 
#prints ziplist to confirm shapefile root names have been added
print ziplist
 
#creates zipefiles in dest folder with basenames
for f in ziplist:
  # prints each itme in the ziplist
  print f
  #creates the name for each zipefile based on shapefile root names
  file_name = os.path.join(dest, f+".zip")
  #print to confirm
  print file_name
  #created the zipfiles with names defined above
  zips = ZipFile(file_name, "w")
  print zips
  #files lists all files with the current basename (f) from ziplist
  files = glob.glob(str(f)+".*")
  # iterate through each basename and add all shapefile components to the zipefile
  for s in files:
    print s
    zips.write(s)
  zips.close()