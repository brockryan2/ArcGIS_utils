import pyodbc

conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=cc-gis-sql;DATABASE=sde_coss_vector;UID=sde;PWD=N0rthl1n3')
cursor = cnxn.cursor()

cursor.execute("select DISTRICT from CITYCOUNCIL_AREA")
row = cursor.fetchone()
print('name:', row[1])