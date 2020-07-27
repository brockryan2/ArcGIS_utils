#Python

##GeoProcessing Snippets

#Shapefile to FC

input_data = "Park"
output_data = r'X:\GIS\SandySpringsConservancy\SandySpringsConservancy.gdb\Parks'

arcpy.management.CopyFeatures(input_data, output_data, None, None, None, None)

# ===========================================================================================================

#Spatial Join

workspace = r'X:\GIS\GIS\Pro Explore\MyProject\MyProject.gdb'
outWorkspace = r'X:\GIS\GIS\Pro Explore\MyProject\MyProject.gdb'

targetFeatures = os.path.join(workspace, "Parcels_2017")
joinFeatures = os.path.join(workspace, "Zero_Addresses_active_072620")

# Output will be the target features, states, with a mean city population field (mcp)
outfc = os.path.join(outWorkspace, "ZeroAddresses_active_072620_SpatialJoinedTo_Parcels_2017")

# Create new fieldmappings and add the two input feature classes.
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(targetFeatures)
fieldmappings.addTable(joinFeatures)

# The output will have the states with the attributes of the cities. Setting the
# field's merge rule to mean will aggregate the values for all of the cities for
# each state into an average value. The field is also renamed to be more appropriate
# for the output.

pop1990FieldIndex = fieldmappings.findFieldMapIndex("POP1990")
fieldmap = fieldmappings.getFieldMap(pop1990FieldIndex)

# Get the output field's properties as a field object
field = fieldmap.outputField

# Rename the field and pass the updated field object back into the field map
field.name = "mean_city_pop"
field.aliasName = "mean_city_pop"
fieldmap.outputField = field

# Set the merge rule to mean and then replace the old fieldmap in the mappings object
# with the updated one
fieldmap.mergeRule = "mean"
fieldmappings.replaceFieldMap(pop1990FieldIndex, fieldmap)

# Delete fields that are no longer applicable, such as city CITY_NAME and CITY_FIPS
# as only the first value will be used by default
x = fieldmappings.findFieldMapIndex("CITY_NAME")
fieldmappings.removeFieldMap(x)
y = fieldmappings.findFieldMapIndex("CITY_FIPS")
fieldmappings.removeFieldMap(y)

#Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc, "#", "#", fieldmappings)

# ===========================================================================================================

#Select by location:

arcpy.env.workspace      = r'X:\GIS\SandySpringsConservancy\SandySpringsConservancy.gdb'
feature_to_be_selected   = "CIP_Lines_SelectByAttributes_ClippedTo_CityLimit"
selection_criteria_layer = "major_Roads"
selection_type           = 'INTERSECT'
distanceNumber           = 20
distanceUnit             = "FEET"
search_distance          = str(distanceNumber) + " " + distanceUnit

arcpy.SelectLayerByLocation_management(feature_to_be_selected, selection_type, selection_criteria_layer, search_distance)

# ===========================================================================================================

#Select by attribute(s)

# Import system modules
import arcpy

# Set the workspace
arcpy.env.workspace = r'X:\GIS\SandySpringsConservancy\SandySpringsConservancy.gdb'
selectable_feature  = "CIP_Lines"
selection_type      = "NEW_SELECTION"
where_clause        = "PROJECT_PHASE IN('CST', 'PE', 'ROW') AND (EST_TOT_COST >= 1000000.0 OR EST_TOT_COST IS NOT NULL) AND PROJECT_TYPE NOT LIKE '%Signal Upgrade%'"
#select only those cities which have a population > 10,000
arcpy.SelectLayerByAttribute_management(selectable_feature, selection_type, where_clause)

# Write the selected features to a new featureclass
arcpy.CopyFeatures_management(selectable_feature, "Parcels_2017_lessThan_7500sqFt")
