# main.py

from flask import Flask, render_template, request, flash, redirect, Response
#from pandas.io import sql
import pandas as pd
import sqlite3 as sql
from sqlite3 import Error
import io
import matplotlib.pyplot as plt
import base64


df = pd.read_csv("data/expenses.csv") # read csv and set to dataframe df
conn = sql.connect("data.db") # connect to sqlite and create database data.db
df.to_sql("expenses", conn, if_exists = "replace") # insert dataframe into sql table called expenses

conn = sql.connect("data.db") # connect to sqlite
df_from_sql = pd.read_sql_query("SELECT * FROM expenses", con=conn) # read sql query into pandas dataframe
#print(df_from_sql)
#print(df_from_sql.dtypes)
conn.close()

#Data manipulation for MATPLOTLIB bar plot - preprocessing data columns
sortedData=df_from_sql.sort_values("date")
sortedData['Month_Year']=pd.to_datetime(sortedData['date']).dt.to_period('M')
monthSum=sortedData.groupby('Month_Year')['price'].sum().to_frame().reset_index().sort_values(by='price')
#preprocess plot data
##x=monthSum['Month_Year']
##y=monthSum['price']
#monthSum.plot.bar(x='Month_Year', y='price')
#print (monthSum)
#exit()

#Data manipulation for MATPLOTLIB pie plot - preprocessing data columns


categorySum=sortedData.groupby('category').sum()
#print (categorySum)
#slicePrice=categorySum['price']
#labels=categorySum['category']
#define autopct for pie chart values
#def pie_slice(slicePrice):
#    return pie_slice
#
#pieplot data
#categorySum.plot.pie(y='quantity', legend=None, autopct='%.1f%%')
#plt.ylabel('')
#plt.show()
#exit()
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

#MATPLOTLIB to show and plot certain statistics - first plot will be total spent in each category
@app.route('/month_price_bar_plot.png', methods=["GET"])
def catPlot():
    #Start data into memory buffer
    barImage=io.BytesIO()
    #Plot data from preprocessed data to get total expenses per month
    monthSum.plot.bar(x="Month_Year", y="price", color="orange", width=0.4, legend=None)
    #Label the x axis of the matplotlib plot
    plt.xlabel("Month and Year")
    #Label the y axis of the matplotlib plot
    plt.ylabel("Total expenses in all categories")
    #Label the title of the matplotlib plot
    plt.title("Total price of all expenses per month")
    #Bring in x-label by using tight layout function from matplotlib
    plt.tight_layout()
    #Save the figure matplotlib bar plot
    plt.savefig(barImage, format='png')
    #Close the plot
    plt.close()
    barImage.seek(0)
    #Encode and decode image byte data
    linkedImage=base64.b64encode(barImage.getvalue()).decode('utf8')
    #Process html template where image source of mont_price_bar_plot is stored
    return render_template('cat_plot.html', plot_url=linkedImage)

@app.route('/cat_pie_plot.png', methods=["GET"])
def piePlot():
    #Start data into memory buffer
    pieImage=io.BytesIO()
    #Plot data from preprocessed data to get pie chart of expenses per category
    categorySum.plot.pie(y='quantity', legend=None, autopct='%.1f%%')
    #Remove y label from pie plot
    plt.ylabel('')
    #Label the title of the matplotlib plot
    #plt.title("Expenses per category")
    #Bring in x-label by using tight layout function from matplotlib
    #plt.tight_layout()
    #Save the figure matplotlib bar plot
    plt.savefig(pieImage, format='png')
    #Close the plot
    plt.close()
    pieImage.seek(0)
    #Encode and decode image byte data
    linkedpieImage=base64.b64encode(pieImage.getvalue()).decode('utf8')
    #Process html template where image source of mont_price_bar_plot is stored
    return render_template('pie_plot.html', plot_url=linkedpieImage)


if __name__ == "__main__":
    app.run()