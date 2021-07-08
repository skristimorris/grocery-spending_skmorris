# tmp.py

db = "/Users/skm/Documents/MHCI/Summer 2021/HCI 584/Project/grocery-spending_skmorris/data/expenses.csv"
df = pd.read_csv(db)


    #form = AddItem(request.form)
    #Save item data on submit button press
 #   if request.method == 'POST' and form.validate():
 #           save_changes()

c = conn.cursor() # create cursor object
c.execute("SELECT * FROM expenses") # execute query to select everything in expenses db
for row in c.fetchall(): # return all results of query
    print(row)


conn = sql.connect("data.db") # connect to sqlite
df_from_sql = pd.read_sql_query("SELECT * FROM expenses", con=conn) # read sql query into pandas dataframe
#print(df_from_sql)
#print(df_from_sql.dtypes)
conn.close()

            #df = pd.read_sql_query("SELECT * FROM expenses", con=conn) # execute query to select everything in expenses db
            #df.to_csv("data/expenses.csv") # write dataframe to expenses.csv file