# main.py

from flask import Flask, render_template, request, flash, redirect
#from pandas.io import sql
import pandas as pd
import sqlite3 as sql
from sqlite3 import Error

df = pd.read_csv("data/expenses.csv") # read csv and set to dataframe df
conn = sql.connect("data.db") # connect to sqlite and create database data.db
df.to_sql("expenses", conn, if_exists = "append") # insert dataframe into sql table called expenses

conn = sql.connect("data.db") # connect to sqlite
df_from_sql = pd.read_sql_query("SELECT * FROM expenses", con=conn) # read sql query into pandas dataframe
#print(df_from_sql)
#print(df_from_sql.dtypes)
conn.close()

app = Flask(__name__)

# FLASK:  INDEX 
@app.route("/")
def index():
    return render_template("index.html")

# FLASK:  ADD ITEM
@app.route('/add_item', methods=["POST", "GET"])
def add_item():
    if request.method == 'POST':
        try:
            conn = sql.connect("data.db") # connect to sqlite
            c = conn.cursor() # create cursor object
            c.execute("INSERT INTO expenses (name, category, price, quantity, date) VALUES (?,?,?,?,?)",
                (request.form["name"],
                request.form["category"],
                request.form["price"],
                request.form["quantity"],
                request.form["date"])) # execute query to select everything in expenses db
            conn.commit() # apply changes
        except:
            print("Error")
        finally:
            conn.close() # close connection
    return render_template("add_item.html")




    

    

# FLASK:  VIEW SPENDING HISTORY
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

