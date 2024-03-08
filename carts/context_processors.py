from .models import Cart, CartItem
from .views import _cart_id

# 95a Here we will be working with two class Cart and CartItem (import them at the top)

def counter(request):
    # 95e(ii) initailzing cart_count variable
    cart_count = 0
    # 95b if we are in the admin site, we dont want to return any value else we will count the cart_items by filtering 
    # 95c it by the session_id we got from the browser _cart_id() function (import this from the view.py file of the cart app)
    if 'admin' in request.path:
        return {}
    else:
        try:
            # 95d _cart_id is imported from view.py file. It is the session_id of the product in cart
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated: # 244a Here we will make a condition that if the user is logged in, then we should be getting the count of the count item for the user and not based on the cart_id in session
                cart_items = CartItem.objects.all().filter(user=request.user) # 244b
            else:
                cart_items = CartItem.objects.all().filter(cart = cart[:1]) # 244c Next we will goto the cart() function in the view.py 245 file of the carts app to make the cart display when the user is logged in.
            # 95d(i) We filter the cartitem table using only one session_id gotten from the cart table
            ## cart_items = CartItem.objects.all().filter(cart = cart[:1]) # We comment this and put it for # 244c
                
            # 95e then we will access the cart item quantity using for loop to obtain the total number of items in the cart
            for cart_item in cart_items:
                # 95e(i) Initiallze cart_count by setting it to 0 then add it up with the quantities
                cart_count += cart_item.quantity
            # 95f If cart does not exist then use an except keyword
        except Cart.DoesNotExist:
            cart_count = 0
            # 95g Then we will go to the settings.py #96 file of the project app to register the context_processor
    return dict(cart_count = cart_count)
