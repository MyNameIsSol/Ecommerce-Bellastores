from django.shortcuts import render, redirect # 277g
from django.http import HttpResponse, JsonResponse # 275b for httpresonse, # 339b for jsonresponse
from carts.models import CartItem # 277d
from .forms import Orderform # 290 We Have Now omport our Orderform class which we used in # 279
import datetime # 294b
from .models import Order, Payment, OrderProduct # 291b for Order and # 317c for Payment and # 322b for OrderProduct
import json # 317b
from store.models import Product # 329b
from django.template.loader import render_to_string  # 331b (i)
from django.core.mail import EmailMessage # 331b (ii)

 
# Create your views here.

# 298 Here we will write the function for our payment page.
def payments(request): # 298b Our payment function

    # 317 We will handle our posted data from js fetch() function
    body = json.loads(request.body) # 317b We will get all the posted details and store them in body variable. We will also import json at the top
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID']) # 317e This will give us the user order using the orderID
    payment = Payment( # 317c We will get the details from the body variable and store them in the Payment() model. We will import the payment model at the top.
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total, # 317d We will get the amount paid from the Order model # 317e
        status = body['status'], # it will be stored as 'successful' as gotton from flutterwave.
    )
    payment.save() # 317f We will now save the payment.
    order.payment = payment # 317g We will update our payment field(foreign key) in the order model
    order.is_ordered = True # 317h This will set is_ordered status to True when we are done with payment
    order.save() # 317i We will save the order(transaction details) into the database.
    # 318 Next will go to the admin.py # 319 of the orders app to add the list of fields we will want the admin to see in the admin area of the (orders table). and not the user seeing only the name of client making order.
    
    # 322 Next we will move the cart items to the ordered product table(order product). Here we will store the ordered products
    cart_items = CartItem.objects.filter(user=request.user) #We will get the cart item by filtering using the user
    for item in cart_items: # We will loop through the user cart_items
        orderproduct = OrderProduct() # We will create the orderproduct object in which we will save the item in its fields of the OrderProduct model. # 322b We will import the OrderProduct model at the top
        orderproduct.order_id = order.id # NB: orderproduct.order_id is the order field(ForeignKey/uniqueId of an order) in the OrderProduct model while we could access the order.id assigned to it because we are getting from the order field in 317e
        orderproduct.payment = payment # We are getting the 'payment' assigned to orderproduct.payment from the payment field in 317c
        orderproduct.user_id = request.user.id # We are accesing the user id and assigning it the user field(ForeignKey) of the OrderProduct models
        orderproduct.product_id = item.product_id # We are getting the product_id from looping the cart_items
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
    # End of # 322
    # NB: We did not store the variation field because its value is a manyTOmany in the Cartitem models. To assign the value, we first have to save the OrderProduct object # 322, then we can now access the variation field and get the value
    # 323 We will first go to the models.py # 324 file of the orders app to delete the size and colour field since we wont be using them but the variations field instead.
    # 325 We will now want the ProductOrder table to stay below the Order table in the admin area. This is called tabular inline. To do this, we will go to the admin.py # 326 of the orders app

    # 328 Here we will fetch the variation from the CartItem and store it in the ProductOrder table
        cart_item = CartItem.objects.get(id=item.id) # We will take the CartItem by the item_id - because we want to take the variation of the partcular cart item
        product_variation = cart_item.variations.all() # We will now take the product variations of the cart item (all variations of the cart item)
        orderproduct = OrderProduct.objects.get(id=orderproduct.id) # Here we can access the ordered products by the orderproduct id we saved in # 322 above
        orderproduct.variations.set(product_variation) # We can now add the product_variation to the orderproduct(ordered product) variation
        orderproduct.save() # we can now save the orderproduct
        # 328 ends

    # 329 Next we will want to reduce the quantity of the sold product
        product = Product.objects.get(id=item.product_id) # So we are using the for loop to get the particular product using the product id. We will import Product at the top # 329b.
        product.stock -= item.quantity # We will then take the stoke from the product. This will reduce the quantity of this particular product
        product.save() # We save the product table. # 329 end
    
    # 330 Next we will want to clear the cart item after order has been made.
    CartItem.objects.filter(user=request.user).delete() # This will delete the cart items for this particular user

    # 331 Next we will send order received email to the user
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_received_email.html', { # import render_to_string # 331b (i) at the top.
        'user': request.user, # We will pass the user details to the template,
        'order': order, # We will also be send the order object.
    }) # Here we will pass the email body(The template or text) for the email, 
    to_email = request.user.email # address to send the email ( a user email)
    send_email = EmailMessage(mail_subject, message, to=[to_email]) # this email function take the parameter for sending an email. NB: import # 331b (ii) EmailMessage at the top
    send_email.send() # This will send the email for us (# 331 ends). We can now create the # 332 order_received_email.html file in the template/orders folder and pass the message parameters to it(user,order)
    
    # 334 We will like to redirect the user to the order complete page, to do this, we will first create a url pattern for it by going to the urls.py fie # 335 of the orders app

    # 338 We will be sending order number and transaction id as a response to our js function in the payments.html file
    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id,
    }
    # 339 We will now comment the return template below, and return a json data instead.
    return JsonResponse(data) # We will import JsonResponse # 339b at the top. This (data) will go to the place were it came, which is the js function in the payments.html file # 340
    # return render(request, 'orders/payments.html') # 298c Next we will create the payments.html file # 299 the function will be taking us to. We will go to the template folder and create a new folder(orders) with the payments.html file in it(templates/orders/payments.html)

# 274 Here we will create the view function for the orders app
def place_order(request, total=0, quantity=0): # 292b We will add the parameter to get the cart_items "total" and "quantity" from the webpage
    # 276 Next we will comment the HttpResponse code for testing the page.

    # 277 Next we will want to check if there is any cart item before the user can stay in the place_order page. If no cart item, we send the user back to the store page.
    current_user = request.user # 277b We are getting the user because the user must have logged in by now.
    cart_items = CartItem.objects.filter(user=current_user) # 277c Next we get the cart items of the user. Import the CartItem model # 277d at the top.
    cart_count = cart_items.count() # 277e This will count the cartitem of the user 
    if cart_count <= 0: # 277f We will check if the cartitem is less than 0, we will return the user to the store page
        return redirect('store') # 277g This will redirct the user to the store page. We will import the redirect method at the top. 
    
    # 292 Here we will write the code to calculate the total, quantity, tax, and grand_total. We will add the parameter to get the cart_items total and quantity in the place_order() fuction at the top
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax # 292 ends

    # 278 Next we will want to receive the user order and collect his billing address details from the post form
    if request.method == "POST":
        form = Orderform(request.POST) # 279 Next will be passing the posted informations into an Orderform function. We wil create our Orderform function by creating a forms.py # 280 file in the orders app and writing the function there.
        if form.is_valid(): # 291 If the form is valid, we can now store the billing information inside the order table
            data = Order() # 291b This create the instance of the order. We will import the Order class at the top.
            data.user = current_user # 291bi This assign the current_user to the user column of the database
            data.first_name = form.cleaned_data['first_name'] # 291c This is how we take the field data from the request.POST (method) past in the Orderform class
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note'] # 291c ends

            # 291d We will also set other field according to the columns(fields) created in the Order model of the models.py file of the orders app
            data.order_total = grand_total # 291e We will write the code to calculate the total, quantity, tax, and grand_total at the top # 292
            data.tax = tax # 291f
            # 293 The status field is by default set to "New" so we dont need to add the field
            data.ip = request.META.get('REMOTE_ADDR') # 293b This will get the user current ip
            data.save() # 293c Then we will save the order and a primary key(id number) will be created automaticaaly

            # 294 Next we will use the primary key(id number) generated above to create our order_number combining our current date, year, month
            yr = int(datetime.date.today().strftime('%Y')) # 294b We will get the current year and then We will import the datatime class above
            dt = int(datetime.date.today().strftime('%d')) # 294c Here we get the current day(date)
            mt = int(datetime.date.today().strftime('%m')) # 294d Here we get the current month
            d = datetime.date(yr,mt,dt) # 294e Here we are getting the year, month, day in this format and will be stored in d variable
            current_date = d.strftime("%Y%m%d") # 294f We will then get the date in this format 20240413

            # 294g Next we will concatenate the primary key with this current_date to get our order_number
            order_number = current_date + str(data.id)
            data.order_number = order_number # 294h We will assign the order_number to its column in the database
            data.save() # 294i We will now store our data.

            # 301 We will get the orders so they can be displayed in the payments.html page
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order, # 301b This will send the order details of # 301 to the payments.html template
                'cart_items':cart_items, # 301c This will send the cart_items details of # 277c to the payments.html template
                'total':total, # 301d This will send the total detail of # 292 to the payments.html template
                'tax':tax, # 301e This will send the tax detail of # 292 to the payments.html template
                'grand_total':grand_total, # 301f This will send the grand_total details of # 292 to the payments.html template
            }
            # 302 Next we will comment the redirect('checkout') of # 294j and write the code to render the context dict on the payments.html # 303 page of templates/orders/payments.html
            return render(request, 'orders/payments.html', context)
            #return redirect('checkout') # 294j Then we will retun to the checkout page.
        
    else: # 294k else we will return to the checkout page if no data was posted. We will now go to the store/checkout.html # 295 of the template folder to include the POST url of our billing form
        return redirect('checkout')

            # Next we will store the data inside our Order model

    # return HttpResponse('OK') # 275 import the httpResponse # 275b at the top of the code the test the page by typing the url 127.0.0.1:8000/orders/place_order

# 336 Here we will write the view function for the order complete page
def order_complete(request):
    # 341 We will get the order parameters from our url which is the order_number and payment_id, then use it to fetch the remaining data to be displayed in the Thank you page.
    order_number = request.GET.get('order_number') # 341b
    transID = request.GET.get('payment_id') # 341c

    try: # 341d
        order = Order.objects.get(order_number=order_number, is_ordered=True) # 341d(i) This will get all the order that has been paid for using the order_number
        ordered_products = OrderProduct.objects.filter(order_id=order.id) # 341d(ii) This will get the products that has been ordered so we can display them
        payment = Payment.objects.get(payment_id=transID) # 341d(iii) This will get the payment using the transID gotton from the GET request.

        # 347 We will get the sub total from ordered_products so that we can pass it to the context object and display it on the order complete page
        subtotal = 0 # 347b
        for i in ordered_products: # 347c
            subtotal += i.product_price * i.quantity # 347d

        context = { # 341e
            'order': order, # 341e(i)
            'ordered_products' : ordered_products, # 341e(ii)
            'payment' : payment, # 341e(iii)
            'order_number': order.order_number, # 341e(iv) we get the order_number form the order table
            'transID' : payment.payment_id, # 341e(v) we get the transID from the payment table
            'subtotal': subtotal, # 348 We will send the subtotal to the order_complete.html # 349 in the template/orders folder
        }
        return render(request, 'orders/order_complete.html', context) # 341f We will comment # 336b and put the redirect here. Then pass the context object in it
    except (Payment.DoesNotExist, Order.DoesNotExist): # 341g(i) We will handle payment does not exist and order does not exist in the except block 
        return redirect('home') # 341g(ii) We will redirect the user to the home page.
    #342 Next we will go to the order_complete.html # 343 in the templates/orders folder to implement the context object.

    # return render(request, 'orders/order_complete.html') # 336b We will go create the order_complete.html # 337 in the templates/orders folder Which will be rendered when the function is called in the url pattern of the orders app