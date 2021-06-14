from wtforms import Form, SelectField, StringField

class AddItem(Form):
    category = [("Bakery", "Beverages", "Candy", "Dairy", "Deli", "Frozen", "Meat", "Produce", "Snacks")]
    name = StringField("Name")
    category = SelectField("Category", choices=category)
    price = StringField("Price")
    quantity = StringField("Quantity")
    date = StringField("Purchase Date")
