# Name: AddField.py
# Description: Add a new field to a table
 
# Import system modules
import arcpy
 
# Set environment settings
workspaceRoot = r'X:\GIS'
projectFolder = r'\PublicSafety_Fire\Projects\Hydrants\2018_Hydrant_Inspections\2018_Hydrant_Inspections_Pro'
gdb = '2018_Hydrant_Inspections.gdb'


arcpy.env.workspace =  workspaceRoot + projectFolder + gdb

# Set local variables
featureClass = "PublicHydrants"
fieldName = "Inspected"
fieldType = "TEXT"  		  # Options = TEXT / FLOAT / DOUBLE / SHORT / LONG / DATE / BLOB / RASTER / GUID (Globally Unique IDentifier)
fieldPrecision = 0			  # The number of digits that can be stored in the field. All digits are counted no matter what side of the decimal they are on
fieldScale = ""				  # The number of decimal places stored in a field. This parameter is only used in float and double data field types.
fieldLength = 10			  # sets the maximum number of allowable characters for each record 
fieldAlias = "Inspected ?"
nullable = "NULLABLE"		  # Specifies whether the field can contain null values
required = "NON_REQUIRED"	  # Specifies whether the field being created is a required field for the table
domain = ""					  # specify the name of an existing domain for it to be applied to the field

 
# Execute AddField to create new field
arcpy.AddField_management(featureClass, fieldName, fieldType, fieldPrecision, fieldScale, fieldLength, fieldAlias, nullable, required, domain)