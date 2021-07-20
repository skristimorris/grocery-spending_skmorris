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



'''
# set this to 1 to recreate or overwrite the SQL with your hand edited csv file
if 0:
    df = pd.read_csv("data/expenses.csv") # read csv and set to dataframe df
    conn = sql.connect("data.db") # connect to sqlite and create database data.db
    df.to_sql("expenses", conn, if_exists = "replace", index = False) # insert dataframe into sql table called expenses
    conn.close()

conn = sql.connect("data.db")
df = pd.read_sql_query("SELECT category, SUM(price) AS price, strftime('%Y-%m', date) AS 'year-month' FROM expenses GROUP BY category, strftime('%Y-%m', date) ORDER BY strftime('%Y-%m', date), category", con=conn)
fig = px.bar(df, x="year-month", y="price", color="category", barmode="group")
print(df)
conn.close()
'''

'''
# callback to add new item to table - SQL
@app.callback(
    Output('output-input-form', 'children'),
    [Input('submit-new-item', 'n_clicks')],
    [State('name', 'value'),
    State('category', 'value'),
    State('price', 'value'),
    State('quantity', 'value'),
    State('date', 'date')
    ]
)
def add_item(n, name, category, price, quantity, date):
    if n:
        try:
            #print(name)
            conn = sql.connect('data.db')
            c = conn.cursor()
            c.execute(
                'INSERT INTO items (name, category, price, quantity, date) VALUES (?,?,?,?,?)',
                [
                name, category, price, quantity, date
                ]
            )
            conn.commit()
        except Error as e:
            print(e)
        finally:
            #print(pd.read_sql_query('SELECT * FROM items', con=conn))
            print(df)
            conn.close()
    #return name, category, price, quantity, date
'''    