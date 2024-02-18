from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

# 71a(iii) we will create a custom CartAdmin
class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id', 'date_added')

# 71a(iv) We will  create a custom CartItemAdmin
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product', 'cart','quantity', 'is_active')

# 71a(i) Here we will register our cart model and cartitem model. Then we will create a custom CartAdmin and CartItemAdmin and also register them, to enable us customize the fields to display in the admin 
# 71a(ii) But first we have to import the models(cart,cartitem) at the top

# 72 We will now make the cart functionality so that when we click the 'add to cart' button 
# of a product in its category page, (127.0.0.1:8000/store/category_slug/product_slug), it will take us 
# to the cart page and also add the product to cart with the help of a session key. So we will go and create 
# a add_cart() function in the views.py # 73 file of the carts app

# 71b We will register our custom CartAdmin and CartItemAdmin
# 71c Then we will refresh our admin site to view the cart and cartitem model
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
