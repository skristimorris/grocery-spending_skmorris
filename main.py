# main.py

#import datetime # imports the date and time - used for users to enter purchase dates in a date format
from flask import Flask, flash, render_template, request, redirect
from forms import AddItem
import pandas as pd
import sqlite3

dbname = "data/expenses.csv" # import data from csv file
df = pd.read_csv(dbname) # read csv and set to dataframe
print(df)



app = Flask(__name__)
@app.route('/forms', methods=["GET", "POST"])
#def test():
#    return "this is a test"
def additem():
    form = AddItem(request.form)
    #Save item data on submit button press
 #   if request.method == 'POST' and form.validate():
 #           save_changes()
    return render_template("new_item.html",form=form)

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

