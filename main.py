# main.py

#import datetime # imports the date and time - used for users to enter purchase dates in a date format
from flask import Flask, render_template, request
#from pandas.io import sql
from forms import AddItem
import pandas as pd
import sqlite3

dbname = "data/expenses.csv" # import data from csv file
df = pd.read_csv(dbname) # read csv and set to dataframe df
print(df)

conn = sqlite3.connect("data.db") # connect to sqlite
df.to_sql("expenses", conn, if_exists = "replace", index = False) # write records stored in df to sql db named expenses, drop table if it exists before inserting new values
c = conn.cursor() # create cursor object
c.execute("SELECT * FROM expenses") # execute query to select everything in expenses db
for row in c.fetchall(): # return all results of query
    print(row)
conn.close() # close connection

conn = sqlite3.connect("data.db") # connect to sqlite
df_from_sql = pd.read_sql_query("SELECT * FROM expenses", con=conn) # read sql query into pandas dataframe
print(df_from_sql)
print(df_from_sql.dtypes)
conn.close()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route('/additem', methods=["GET", "POST"])
def additem():
    form = AddItem(request.form)
    #Save item data on submit button press
 #   if request.method == 'POST' and form.validate():
 #           save_changes()
    return render_template("add_item.html",form=form)

@app.route('/spending_history')
def spending():
    return render_template("spending_history.html")

#Save Data
#def save_changes(Expense, form, new=False):
#    name = name()

#Display pandas table in html
#@app.route('/expenses')
#def display_expenses():
#    data= pd.read_csv("/Users/skm/Documents/MHCI/Summer 2021/HCI 584/Project/grocery-spending_skmorris/data/expenses.csv", sep='\s+', quotechar='"')
#    data.set_index(['Name'], inplace=True)

#    return render_template(data)


if __name__ == "__main__":
    app.run()




#Enter Date of item
#Purchase_Date=input('Enter the date the item was purchased: ')
#Purchase_Price=input('Enter the price of the item: ')
#df2=df.append({'Purchase Date': Purchase_Date,'Purchase Price': Purchase_Price }, ignore_index=True)

#print(df2)

