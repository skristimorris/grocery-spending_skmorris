# User Guide
The **Grocery Spending App** offers personal insights into a user's grocery spending habits by tracking their purchased grocery items. Users are able to analyze their grocery transactions at an item level by using the interactive dashboard that is by filtered by month and category.  

## Requirements
The packages and corresponding versions are listed below and can be found in the ```requirements.txt``` file.

Package | Version
--------|--------
Dash | 1.20.0
Dash Bootstrap Components | 0.12.2
Dash Core Components | 1.16.0
Dash HTML Components | 1.1.3
Dash Table | 4.11.3
Pandas | 1.2.4
Plotly Express | 0.4.1
Python | 3.8.8

## Installation
Prior to running ```app.py```, use pip to install the required third party packages:
``` 
pip install -r requirements.txt
```
## Usage
After installing the required packages, open an IDE and run ```app.py```.

The terminal will display the following:
>Dash is running on http://127.0.0.1:8050/

## Known Issues
Below are known issues:
* The app runs off a CSV file with queries to the Pandas dataframe.
* There is no authentication function.
* The app does not allow multiple users.
* The slider input for quantity only goes up to 10.
* The item name is not capitalized in the CSV file if it is entered in all lowercase letters.
* The format of the amount in the pie chart is longer than two decimals.
* The amount at the top of the bar chart is cut off at the top.
