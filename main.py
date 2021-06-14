# main

# imports the date and time - used for users to enter purchase dates in a date format
import datetime

# import flask
from flask import Flask
# test flask
app = Flask(__name__)

@app.route('/')
def test():
    return "Welcome to Flask!"

#define app in flask
#main = Flask(__name__)

# import csv data files
import pandas as pd # access to pandas-defined objects is done via pd
df = pd.read_csv("/Users/skm/Documents/MHCI/Summer 2021/HCI 584/Project/grocery-spending_skmorris/data/expenses.csv")
#print(df) # show formated with leading index row

#Enter Date of item
#Purchase_Date=input('Enter the date the item was purchased: ')
#Purchase_Price=input('Enter the price of the item: ')
#df2=df.append({'Purchase Date': Purchase_Date,'Purchase Price': Purchase_Price }, ignore_index=True)

#print(df2)

