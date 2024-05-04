from django import forms
from .models import Order

# 280 Here we will create our Orderform() class
# 280b We will import the forms model at the top to in order to create our Orderform() class
# 280c We will also import the Order model into this file
class Orderform(forms.ModelForm): # 280d We are inheriting all functionality of the python forms model then we can also add our own code in our Orderform() class
    class Meta: # 280e We will use this to list the field we want to get the form details from the place_order POST data then we will go back to our views.py file # 290 of the orders app to import our Orderform class
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']