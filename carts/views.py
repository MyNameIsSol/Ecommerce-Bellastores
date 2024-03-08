from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required # 231b import the login required decorator

# Create your views here.

# 73e(i) We will create a private(using underscore(_) before func name) function _cart_id() to get the product session_id on the web browser which will be stored in our cart table.
# 73e(ii)The function will take request as an argument to get the product session_id which will be the cart_id
def _cart_id(request):
    # 73e(iii)session_key means session_id
    cart = request.session.session_key
    # if there is no session(cart variable) at all, we are going to create a new session and return the cart(as cart_id)
    if not cart:
        cart = request.session.create()
    return cart


# 73a We will create a add_cart() function and pass the request argument 
# 73b and since we are going to add the product into the cart, we will also pass the product_id as an argument
def add_cart(request, product_id):
    # 73c Next we will get the product(import the product model at the top) from the product model(table) using the product_id argument
    product = Product.objects.get(id=product_id)

    # 246 When the user logout and select the same item, when he login to checkout, we want to be able to check if he has that product already, then add it to the saved one and not creating the same product again.
    if request.user.is_authenticated: # 247 We will check if the user is authenticated, then we will group the items. put the code # 133e to # 75e under the (else statement) and also in the (if statement). but remove all comment in the (if statement) and edit
        
        # our list to store the product variation
        product_variation = []
        # We will receive the variation from the user and add it to cart
        if request.method == 'POST':
            # We will loop through our post request so we can handle and receive any variations coming through i.e brands
            for item in request.POST: # Will loop any value coming from the request POST
                #  color, size, brand will be stored here as key
                key = item
                #  black, medium, gucci will be stored here as value
                value = request.POST[key]
                # print(key, value)  # print to see posted value in terminal

                # We will check if the variations coming from the 'add to cart' POST request is same with the selected product Variations(import the model at the top) in our database, before we can add the product to cart
                try:
                    # This give us the variation values for the specific product i.e blue , medium. We can now store it in a list so we can add as many products as we want
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    # We will append the variation values into the list, then go to the models.py # 114 file of the carts app to add a variation field to the CartItem Model(class)
                    product_variation.append(variation) 
                except:
                    pass

    
        # want to add to the cart already exit with the same variation. if it already exit, we just increase 
        # the quantity of the product in cart else we create a new cart item.
        
        # 248b is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        is_cart_item_exists = CartItem.objects.filter(product=product, user=request.user).exists() # 248 Since the user is logged in, we will use this code to check if the cart exist for the user and comment the code above.
       
        if is_cart_item_exists: #  So if cart item exist, we will get the cart_item as
            #  we will access the product table and cart table which are foreignkey to Cartitem table where they equal the add_cart() function product variable and cart variable
            
            # 249b cart_item = CartItem.objects.filter(product=product, cart = cart)
            cart_item = CartItem.objects.filter(product=product, user=request.user) # 249 We will also comment the code above and use this to get the cart items since the user is logged in

            ex_var_list = [] #  We created an empty list to hold all existing variations in the cart_item table
            id = [] #  We created an empty list to hold all cart_item id already in the cart_item table
            for item in cart_item:
                existing_variation = item.variations.all() #  We get all existing variation in the cart_item table
                ex_var_list.append(list(existing_variation)) # We store all variations already in the cart_item table in this list
                id.append(item.id) # We store all cart_item id in the the cart_item table in the id list

            if(product_variation in ex_var_list): #  We check if the posted product has been added to the cart with same variation 
                index = ex_var_list.index(product_variation) #  We get the id of the posted product using the index number of its product variation   
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id) #  We check if the posted product is already in cart
                item.quantity += 1 #  We increment the quantity of the cart_item
                item.save()
            else: #  We will create a new cart_item and update # 115 from (cart_item.variations) to (item.variations)
                #  when you refresh the browser, you will notice that it is not adding the variations to the product you are inceasing the quantiity using the + sign.
                
                # item = CartItem.objects.create(product=product, quantity=1, cart=cart) # 250b
                item = CartItem.objects.create(product=product, quantity=1, user=request.user) # 250 We will also comment the code above and use this instead to create the cart since the user is logged in

                #  Now we wiil add the product variation inside the database
                #  we will first check if the product_variation =[] list is empty, and if it is empty, we will just update the quantity of the cart_item and if it is not empty, we are going to increase the cart item quantity and save it with its variation
                if len(product_variation) > 0:
                    item.variations.clear() # We will clear the previous cartitem variation so we can add a new one
                    item.variations.add(*product_variation)  # this will add the posted variations to the cart_item variation field. * makes sure it add all the product variation we are posting
                item.save()

            #  We commented the except: block to replace with else:
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product = product,
                #  quantity will be 1 cuz its a new cart_item
                quantity = 1,
                # cart = cart, # 251b
                user = request.user, # 251 We will comment the code above and use the user to create the cart since the user is logged in
                                    # 252 Now when the user is loggedin, and he add the same item with same variation, it is increasing the quantity(grouping). 
                                    # What we will do next is to make it group also when the user logout, then select an item and login again. To achieve this, we will go to the login() function of the views.py # 253 file in the account app
            )

            #  When we dont have this product in cart, we should add a new product with its variation
            #  we will first check if the product_variation =[] list is empty, and if it is empty, we will just add a new cart_item and if it is not empty, we are going to add the item to cart with its variation
            if len(product_variation) > 0:
                cart_item.variations.clear() # We will clear the previous cartitem variation so we can add a new one
                cart_item.variations.add(*product_variation)  # this will add the posted variations to the cart_item variation field. * makes sure it add all the product variation we are posting

            # save the cart_item
            cart_item.save()
        return redirect('cart')            
    else: # 247b

        # 113e our list to store the product variation
        product_variation = []
        # 113a We will receive the variation from the user and add it to cart
        if request.method == 'POST':
            # 113a(i) comment the post request so we can loop and get key : value
            # color = request.POST['color']
            # size = request.POST['size']
            # end 113a(i)

            # 113b We will loop through our post request so we can handle and receive any variations coming through i.e brands
            for item in request.POST: # Will loop any value coming from the request POST
                # 113b color, size, brand will be stored here as key
                key = item
                # 113b black, medium, gucci will be stored here as value
                value = request.POST[key]
                # print(key, value)  # print to see posted value in terminal

                # 113c We will check if the variations coming from the 'add to cart' POST request is same with the selected product Variations(import the model at the top) in our database, before we can add the product to cart
                try:
                    # 113d This give us the variation values for the specific product i.e blue , medium. We can now store it in a list so we can add as many products as we want
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    # 113f We will append the variation values into the list, then go to the models.py # 114 file of the carts app to add a variation field to the CartItem Model(class)
                    product_variation.append(variation) 
                except:
                    pass



        # 73d(i) We will make a try block to get a cart (import the Cart class at the top) by cart_id (cart model) that is equal to or matches the product session_id in 
        # 73d(ii) the cookies of the web browser (we will get this product session_id using a function called cart_id())
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request)) # get the cart using the key present in the session
            # 73f An except keyword used to handle when a cart does not exist so we can create a new cart and save it
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

    # 73g(i) Now that we have a Product and a Cart, we will want to save this Product inside the Cart so it will become our CartItem. 
    # 73g(ii) So that in one Cart, there can be multiple products(Cartitems)
    # 73g(iii) We will combine this product(variable) and cart(variable) so we can get the cartitem(import the CartItem class at the top). we will use a try block for this

    # 117a We will comment the try: exception: block and replace it with an if: else: statement, to check if the product we 
    # want to add to the cart already exit with the same variation. if it already exit, we just increase 
    # the quantity of the product in cart else we create a new cart item.
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists() # 117a(ii)
        # try:
        if is_cart_item_exists: # 117a(iii) So if cart item exist, we will get the cart_item as # 74a
            # 74a we will access the product table and cart table which are foreignkey to Cartitem table where they equal the add_cart() function product variable and cart variable
            cart_item = CartItem.objects.filter(product=product, cart = cart)

            ex_var_list = [] # 118a(i) We created an empty list to hold all existing variations in the cart_item table
            id = [] # 118a(ii) We created an empty list to hold all cart_item id already in the cart_item table
            for item in cart_item:
                existing_variation = item.variations.all() # 118a(iii) We get all existing variation in the cart_item table
                ex_var_list.append(list(existing_variation)) # 118a(iv) We store all variations already in the cart_item table in this list
                id.append(item.id) # 118a(v) We store all cart_item id in the the cart_item table in the id list

            if(product_variation in ex_var_list): # 119a We check if the posted product has been added to the cart with same variation 
                index = ex_var_list.index(product_variation) # 119a(ii) We get the id of the posted product using the index number of its product variation   
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id) # 119a(iii) We check if the posted product is already in cart
                item.quantity += 1 # 119a(iv) We increment the quantity of the cart_item
                item.save()
            else: # 120a(i) We will create a new cart_item and update # 115 from (cart_item.variations) to (item.variations)
                # 120a(ii) when you refresh the browser, you will notice that it is not adding the variations to the product you are inceasing the quantiity using the + sign. 
                # In other words, we need the fix the quatity increment button(+) and the quantity decrement button(-). to fix this, we go to the cart.html # 121 page  
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)

                # 115a(i) Now we wiil add the product variation inside the database
                # 115a(ii) we will first check if the product_variation =[] list is empty, and if it is empty, we will just update the quantity of the cart_item and if it is not empty, we are going to increase the cart item quantity and save it with its variation
                if len(product_variation) > 0:
                    item.variations.clear() # We will clear the previous cartitem variation so we can add a new one
                    item.variations.add(*product_variation)  # this will add the posted variations to the cart_item variation field. * makes sure it add all the product variation we are posting
                item.save()

                # 120a(ii) We will comment # 74b and # 74c code
                # 74b cart_item quantity should be incremented by one(1) when we click the 'add to cart' button
                # cart_item.quantity += 1  # 74b code   # cart_item.quantity equals cart_item.quanty + 1
                # 74c Save the cart_item
                # cart_item.save() # 74c code
                # 75a(i) We will add an except keyword to handle when a cart does not exist yet. We will store the add_cart() 
                # 75a(ii) function product variable and cart variable in the product and cart field of the CartItem table

            # 117a(ii) We commented the except: block to replace with else:
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product = product,
                # 75b quantity will be 1 cuz its a new cart_item
                quantity = 1,
                cart = cart,
            )

            # 115b(i) When we dont have this product in cart, we should add a new product with its variation
            # 115b(ii) we will first check if the product_variation =[] list is empty, and if it is empty, we will just add a new cart_item and if it is not empty, we are going to add the item to cart with its variation
            # 115c Next we will go to the cart.html # 116 file to display the variations among the product details.
            if len(product_variation) > 0:
                cart_item.variations.clear() # We will clear the previous cartitem variation so we can add a new one
                cart_item.variations.add(*product_variation)  # this will add the posted variations to the cart_item variation field. * makes sure it add all the product variation we are posting

            # 75c save the cart_item
            cart_item.save()
            # 75d then we will redirect(import the redirect method at the top) the user to the cart page
            # 75e Next we will create the add_cart() method url in the urls.py # 76 file of the cart app
        return redirect('cart')

# 85a We will write a function to decrement a cart item quantity using the minus(-) button on the cart page.
# 122a We will add a new parameter 'cart_item_id' to the remove_cart function.
def remove_cart(request, product_id, cart_item_id ):
    # 85b we will get the cart item using the product session_id we got using the _cart_id() method
    ## cart = Cart.objects.get(cart_id = _cart_id(request))
    # 85c we will get the product with the help of the get_object_or_404()(to be imported at the top) using the product_id received as an argument in the function
    product = get_object_or_404(Product, id=product_id)

# 122b Next we will make a try block and move code 85d and 85e inside
    try:
    # 258 Will like to handle cart decrement for the logged in user. 
        if request.user.is_authenticated: # 258b We check if the useris looged in 
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id) # 258c We will get the user associated to the cart item
        else: # 258d We will comment # 85b code and # 122c code then copy them into this else statement. Next we will fix the Remove button so logged in user can remove cart item. To do this we will go to the remove_cart_item() # 259 function below
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    # 85d We will get the cart_item that matches the product_id from the browser and also that matches the 
    # session_id from the browser.
    # 122c We will add a new key=value(id=cart_item_id) argument to the CartItem get function to get the actual cart item and leave the rest of the code as it is.
    # 122d Next we will go to the cart.html # 123 file and modify the decreasing(-) cart quantity button.
            
        ## cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        # 85e if cart_item.quantity is > 1 then we should be able to decrement the quantity by 1 otherwise we will delete this cart item
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
# 122b(ii) We the add our except block and ignore the expressing using the pass keyword.
    except:
        pass
    # 85f We will now redirect to the cart page then go to the urls.py # 86 to add a path() that will call the remove_cart() function
    return redirect('cart')


# 87a We will write the function to remove cart item
# 127 We will add a new parameter (cart_item_id) to the remove_cart_item() function to get the cart item id.
def remove_cart_item(request, product_id, cart_item_id):
    ## cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    # 259 We will make the logged in user able to remove cart item
    if request.user.is_authenticated: # 259b We check if the user is logged in 
        cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id) # 259c We get the user associated with the cart item
    else: # 259d We will comment Cart variable in line 260 and also # 127b code then copy them and put in this else statement. Next Will want that when the user click the checkout button and he is force to loggin, When he log in, he should be directed back to any page that comes after next/appname on our webpage url and not a page forced in the view.py # 260 file of the account app i.e (dashboard page). 
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)

    # 127b We will add a key=value(id=cart_item_id) parameter to the CartItem model get() function to get the particular cart item, then the rest of the code remains.
    # 127c If we refresh our browser and click the remove button in the cart page, you will see our remove button now works fine. Now let go to the cart.html # 128 and add a JS to the remove button
    ## cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)

# 87b this will delete the selected cart_item. Next we need to add the url path to this function 
# remove_cart_item() in the urls.py #88 file of the cart app
    cart_item.delete()
    return redirect('cart')

# 68 Here we will then create the view function cart() to render(import the render functon at the top) 
# our cart page(cart.html) to the browser then we will go to our template/store folder to create our cart.html # 69 file
# modified as # 78 but should be used like this when we get to # 68
# def cart(request):
#     return render(request, 'store/cart.html')


# 78 We modify the cart() function to be able to display the cartitem details on the cart page
def cart(request, total=0, quantity=0, cart_items = None):
    try: 
        tax = 0
        grand_total = 0
        # 245 So we will add condition to check if the user is logged in so we will display the cart items assigned to the user and not using the cart_id in the session
        if request.user.is_authenticated: # 245b
            cart_items = CartItem.objects.filter(user=request.user, is_active = True) # 245c
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # 245d
            cart_items = CartItem.objects.filter(cart=cart, is_active = True) # 245e A problem we will fix now is that if we logout and add the same product with same variation, the quantity of the product should increase(be grouped) instead it is adding a new item to the cart. to correct this, we will go to the add_cart() # 246 function at the top

        # 78b We will get the card_id(product session_id of the browser stored in the Cart table)
        ## cart = Cart.objects.get(cart_id = _cart_id(request)) # We will comment this for # 245d
        # 78c  We wiil get the cart_items that matches the card_id above
        ## cart_items = CartItem.objects.filter(cart=cart, is_active = True) # We will comment this for # 245e
        
        # 78d We will loop throught cart_items so we can print them and calculate total amount
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        # 82a We will calculate for two percentage of tax on the total amount
        tax = (2 * total)/100
        # 82b we will calculate for grand_total
        grand_total = total + tax

        # 78e We will use the except keyword with the ObjectDoesNotExist class(import this class at the top) to pass and continue if the object does not exit
    except ObjectDoesNotExist:
        pass
        
        # 78f We will create a context dictionary to pass the values to the cart template then we will go to 
        # the cart.html # 79 file to display our cart
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items, 
        # 83 we will send the tax and the grand_total to the cart.html # 84 file
        'tax' : tax,
        'grand_total' : grand_total
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login') # 231a Here we will import the login_required decorator # 231b at the top, then we will add it here at the top of the checkout() function to force the user login before checkout. 
                                    # Next we will want the "place order" button to save the billing address in the checkout page. To do that, we will go to the checkout.html # 232 file to modify the form for POSTING date.
# 216 Here we will create our checkout function
#def checkout(request): # 225 We will comment this function name, and recreate the fuction with more argument
def checkout(request, total=0, quantity=0, cart_items = None): # 226 We will add other aguments to the fuction just like the cart function
    # 224 Here we will add the functionality to display the cart item in the checkout page.
    try: 
        tax = 0
        grand_total = 0

         # 161 Here we will comment # 227a and # 227b code then we will add condition to check if the user is logged in so we will display the cart items assigned to the user and not using the cart_id in the session
        if request.user.is_authenticated: # 161b
            cart_items = CartItem.objects.filter(user=request.user, is_active = True) # 161c
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # 161d
            cart_items = CartItem.objects.filter(cart=cart, is_active = True) # 161e Now if we refresh the checkout page, we will see the cart items. Next we will want the place order button to be functional. To do that, we will first create and order app which we will then create the models(tables) to store the order informations. 

        # 227a We will get the card_id(product session_id of the browser stored in the Cart table)
        # cart = Cart.objects.get(cart_id = _cart_id(request))
        # 227b  We wiil get the cart_items that matches the card_id above
        # cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        
        # 227c We will loop throught cart_items so we can print them and calculate total amount
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        # 227d We will calculate for two percentage of tax on the total amount
        tax = (2 * total)/100
        # 227e we will calculate for grand_total
        grand_total = total + tax

        # 227f We will use the except keyword with the ObjectDoesNotExist class(import this class at the top) to pass and continue if the object does not exit
    except ObjectDoesNotExist:
        pass
        
        # 227g We will create a context dictionary to pass the values to the cart template then we will go to 
        # the checkout.html file to display our cart
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items, 
        # 227h we will send the tax and the grand_total to the checkout.html file
        'tax' : tax,
        'grand_total' : grand_total
    }
    # 216b This will take us to the checkout page. So we will need to ctreate the checkout.html # 217 page by going to the template/store folder and creating the file
    # return render(request, 'store/checkout.html') # 227i We will comment this and render a different one, passing the context dictionary
    return render(request, 'store/checkout.html', context) # 227j We will pass the context dictionary to display the cart items in the checkout.html # 228 file