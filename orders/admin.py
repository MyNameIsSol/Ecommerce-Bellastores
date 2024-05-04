from django.contrib import admin
from .models import Payment, Order, OrderProduct # 270ai

# 326 Next we will add the ProductOrder table below the Order table(This will enable us see all the product associated to a particular order) by creating a OrderProductInline class and assinging the OrderProduct class to a model variable. 
class OrderProductInline(admin.TabularInline):
    model = OrderProduct 
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered') # This will make the fields not to be editable because they are important for the user
    extra = 0 # This will remove the extra rows always created in the inline tabular
# 326 ends
# 327 Next we will want the product variation to be selected in the ProductOrder table. To do this, we will go to the views.py # 328 of the orders app to fetch the variation from the CartItem and store it in the ProductOrder table

# 319 Here we will add the list of fields we will want the admin to see from the orders table when an order is made by a client
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    # NB: The full_name field is a function added inside the order model which concatenate the first_name and last_name
    list_filter = ['status', 'is_ordered'] # This filter the table using this fields.
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email'] # This allow us to search for orders using the data in this fields
    list_per_page = 20 # This helps us show only 20 record in one page.
    # 319 ends. 
    # 321 Next We will go back to the views.py # 322 file of the orders app to move the cart item to the product order table
    
    inlines = [OrderProductInline] # 327 We will now add the OrderProductInline to the inline variable of the OrderAdmin class.
     

# Register your models here.

# 270a Here we will register our created models. But we will first import the models at the top.
admin.site.register(Payment) # 270b We will register the Payment model
admin.site.register(Order, OrderAdmin) # 270c We will register the Order model / # 320 We will now register the OrderAdmin
admin.site.register(OrderProduct) # 270d We will register the OrderProduct model. Next we will want the placeOrder button in the checkout page functional, so that when we click on it, it the store the user billing address form and place the order. To do this, we will create a url pattern for the placeOrder button by going to the urls.py # 271 file of the project(bellastores) app


