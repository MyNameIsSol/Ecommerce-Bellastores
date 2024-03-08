from django.urls import path
from .import views

# 65 We will go to the url.py # 66 file of the project app and add the carts app path
# 67 Next We will import the path function into this file, then create a urlpattern to route 
# to and display the views function(import the views.py file of the cart app at the top) in the views.py # 68 file of the cart app

urlpatterns = [
    path('', views.cart, name='cart'),
         
    # 76 We will create the add_cart() method path(url) then go to the product_detail.html # 77 file and include a url link to the 'add to cart' button
    path('add_cart/<int:product_id>/', views.add_cart, name = 'add_cart'),
    
    # 86a We will add the path() function to call the remove_cart() function in the views.py file 
    # 86b Then we will go to the cart.html # 87 file add include the remove_cart url in the decrement(-) quantity button to decrement the quantity by 1
    # 124 We will now add a new path parameter( <int:cart_item_id> ) to the romove_cart path. Next we will fix the remove button by going to the cart.html # 125 file.
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name = 'remove_cart'),
         
    # 88 We will add the url path to the remove_cart_item() method in the views.py file, then we will go to the cart.html # 89 file to include the remove_cart_item function in the remove button
    # 126 We will now add a new path parameter( <int:cart_item_id> ) to the remove_cart_item path. Next we will go to the views.py # 127 file of the carts app to modify the remove_cart_item() function.
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name = 'remove_cart_item'),

    # 215 Here we will create the url path to our checkout 
    path('checkout/', views.checkout, name='checkout'), # 215b Next we will go to the views.py # 216 file of the carts app to create the checkout function
]