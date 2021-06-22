# db.py

import pandas as pd
import sqlite3 as sql
from sqlite3 import Error

#Print entire dataframe to understand data manipulation _ DELETE - only for testing entire dataframe - will slow down program
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
#Delete above - testing only

conn = sql.connect("data.db")
c = conn.cursor() # create cursor object
c.execute("SELECT * FROM expenses") # execute query to select everything in expenses db
for row in c.fetchall(): # return all results of query
    print(row)
conn.close()


# READ SQL INTO DATAFRAME
conn = sql.connect("data.db") # connect to sqlite
df_from_sql = pd.read_sql_query("SELECT * FROM expenses", con=conn) # read sql query into pandas dataframe
print(df_from_sql.sort_values("date"))
sortedData= df_from_sql.sort_values("date")
#print(df_from_sql.dtypes)
conn.close()

#function for main to get updated data for plotting
#potential preprocessing of data
#def updatedData():
#    return self.sortedData