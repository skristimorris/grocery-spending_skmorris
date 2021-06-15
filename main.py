# main.py

#import datetime # imports the date and time - used for users to enter purchase dates in a date format
from flask import Flask, flash, render_template, request, redirect
from forms import AddItem
import pandas as pd

db = "/Users/skm/Documents/MHCI/Summer 2021/HCI 584/Project/grocery-spending_skmorris/data/expenses.csv"
df = pd.read_csv(db)

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
#def test():
#    return "this is a test"
def additem():
    form = AddItem(request.form)
    return render_template("new_item.html",form=form)

if __name__ == "__main__":
    app.run()




#Enter Date of item
#Purchase_Date=input('Enter the date the item was purchased: ')
#Purchase_Price=input('Enter the price of the item: ')
#df2=df.append({'Purchase Date': Purchase_Date,'Purchase Price': Purchase_Price }, ignore_index=True)

#print(df2)

