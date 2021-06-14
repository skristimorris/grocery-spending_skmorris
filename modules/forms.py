from wtforms import Form, SelectField

class AddItem(Form):
    choices = [("Bakery", "Beverages", "Candy", "Dairy", "Deli", "Frozen", "Meat", "Produce", "Snacks")]
    select = SelectField("Category:", choices=choices)