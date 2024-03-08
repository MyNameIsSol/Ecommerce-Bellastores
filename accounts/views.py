from django.shortcuts import render, redirect # 161 (redirect)
from .forms import RegistrationForm
from .models import Account  # 151b
from django.contrib import messages, auth # 161 import messages, #168b import auth
from django.contrib.auth.decorators import login_required # 171b import login_required
from django.http import HttpResponse # 177bi import httpresponse

# 172 & #200f imported libraries for verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage # 172 & #200f imports end

from carts.views import _cart_id  # 240a this will import the cart id into this file for us.
from carts.models import Cart, CartItem # 240b this will import the Cart class and the CartItem class
import requests # 160b

# Create your views here.

# 131a import the render module at the top if not already imported, then create the register function
def register(request):
    # 150 We will add the code to handle our registration submittion
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # This will contain all the field values
        if form.is_valid(): # If form contains all the required fields, run code in if statement(to craete a user)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0] # Because we dont have a field bringing the username i.e we want to create username for the user, we use the first part of the email to create a username.(Note you can also allow the user create a username for themself)
            # 151 Next we will import the Account model at the top # 151b and create a user(user object) by using the create_user() function we created in the django authentication(accounts.models.py).
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            # 152 Because in our create_user() function in the accounts(model.py) we didnt include creating phone_number field for the user, we can create the phone number like so after the create_user(user) object and then save.
            user.phone_number = phone_number
            user.save()

            # 172 Here we will send an activation eamil to the user which will contain a token so that the link will automatically get expired after the verification is done.
            # First we need to first get the current site, then generate the token.
            current_site = get_current_site(request)# Here we get the current site, right now we are using localhost, but in future we will be using a domain, so we need to write our code to satisfy our future use. NB: import # 172b current_site at the top
            mail_subject = 'Please activate your acccount'
            message = render_to_string('accounts/account_verification_email.html', { # import 172c render_to_string at the top
                'user': user, # We will pass the user details to the template,
                'domain': current_site, # We will pass the current_site (site domain) to the template
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)), #then pass the user primary key by encoding it so that no one will see the details of the primary key. we will decode it when we want to use it (when activating the account). NB: import # 172d urlsafe_base64_encode and force_bytes at the top
                'token': default_token_generator.make_token(user), # this is a default token generator which will help us create a token of the user. NB: import # 172e default_token_generator at the top
            }) # Here we will pass the email body(The template or text) for the email, 
            to_email = email # address to send the email ( a user email)
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # this email function take the parameter for sending an email. NB: import # 172f EmailMessage at the top
            send_email.send() # This will send the email for us (# 172 ends). We can now create the # 173 account_verification_email.html file in the template/accounts folder and pass the message parameters to it(user,domain,uid,token)

            # 161 We will send a success message to register.html on sucessful registration by importing 'messages' and 'redirect' at the top and writing the code below.
            # messages.success(request, 'Thank you for registering with us. We have sent a verification email to your email address. Please verify it.') # 178 because we have only four minute to read this message, we are going to use a different approach to display it. we will comment this
            # return redirect('register') # 161 end # 178b we will comment this also.

            # 179 We will pass the login url instead cuz we will return the user to the login page and then inform him to go to his email and click the verification link
            return redirect('/accounts/login/?command=verification&email='+email) # 180 after we have pass the link, we can now go to the login.html in accounts/template # 181.
            
    else: # 153 then we indent "form = RegistrationForm()" below the else statement
          # 153b Next we will go to the register.html # 154 to display the field_error and non_field_error.
                        
    # 140 We will import the RegistrationForm class at the top, then create a form object and context variable, then pass the context variable holding the forms to the register.html # 141 in render()
        form = RegistrationForm()
    context = {
        'form':form,
    }
    # 131b
    return render(request, 'accounts/register.html', context)

# 132 create the login function
def login(request):

    # 168 we receive the login details by first checking if there is a post request from the login page
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        #NB: This is the user we use in 243b
        user = auth.authenticate(email=email, password=password) # 168b we will import 'auth' at the top from django.contrib
        if user is not None:
            # 238 We want that when we click the login button, after it checks the neccessary cridentials, email and pass. It should also check if the user has anything in the cart, and if there is an item there, it will assign the user to the cart item. 
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # 239 We will use the cart id gotten from the web browser to check if the id exist in the cart table 
                                                                    # NB: the function to get the cart id from the web browser is already written in the views.py # 73eii file of the cart app, 
                                                                    # we will just import the function '_cart_id()' # 240a at the top. We will also import the 'Cart and CartItem' model # 240b at the top to be able to use them here.
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() # 241 Next we use the cartid to check if the items exist in the cartitem table
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart) # 242 Next we will get all the items assigned to the cartid from the browser

                    # 253 Here we will write the code to handle grouping the cart item when the user is logged in
                    # Here in 253 we get all the variation associated to the item by cart id from the newly selected item
                    product_variation = [] # 253b We will create an empty variation list
                    for item in cart_item: # 253c We will loop through the cart item in # 242 to get each item in the cart
                        variation = item.variations.all() # 253d We will get all the variation associated to this item the user have selected 
                        product_variation.append(list(variation)) # 253e Next we will append the variation into an array and make it a list because by defalt, it is a query set.

                    cart_item = CartItem.objects.filter(user=user) # 254 Here we will get the cart items of this user so we can get his product variations
                    ex_var_list = [] # 254b we create an empty array to store existing variation gotten for the items in the user cart
                    id = [] # 254c
                    for item in cart_item: # 254d We will loop through the cart item the user already have
                        existing_variation = item.variations.all() # 254e We are getting all the variation associated to each item the user have selected previously
                        ex_var_list.append(list(existing_variation)) # 254f We are appending the variation as a list in the ex_var_list array
                        id.append(item.id) # 254g We are appending the item id to the empty id array we crated earlier.

                    for pr in product_variation: # 255 We will check the the newly selected cart item with variation is already in the user ex_var_list
                        if pr in ex_var_list: # 255b if the newly selected product variation is in the ex_var_list(The one stored for the user before)
                            index = ex_var_list.index(pr) # 255c We will get the position where the new product variation is found in the ex_var_list
                            item_id = id[index] # 255d this will give use the id of the item
                            item = CartItem.objects.get(id=item_id) # 255e This will use the item id to get the item.
                            item.quantity += 1 # 255f If the item with same variation exist, we increase the item quantity
                            item.user = user # 255g We assign the user to the cart item
                            item.save() # 255h We save the item.
                        else: # 256
                            cart_item = CartItem.objects.filter(cart=cart) #256b if the if statement fails, we will save the cart item. meaning that the user does not have the item in his cart before.
                            for item in cart_item: # 256c This part, we will comment # 243a to # 243c and use it here
                                item.user = user # 256d
                                item.save() 
                                # 257 Next we will want to fix the decrement cart item when the user is logged in. To do this we will go to the remove_cart() function in the views.py # 258 file of the carts app
                        
                    # for item in cart_item: # 243a This assigns the user to each cart item
                        # item.user = user # 243b
                        # item.save() # 243c Now after we have assign the cart item the user, the cart page still shows empty and the cart page count appears as zero. 
                                    # we will first correct the cart page count by going to the counter() function in the content_processor.py # 244 file of the carts app
            except:
                pass

            auth.login(request, user)
            # return redirect('home')
            messages.success(request, 'You are now logged in.') # 187b after we add the message success we can now go to the dashboard.html # 188 in templates/accounts
            #160b return redirect('dashboard') # 187 We will comment redircting to home above and instead, redirect to dashboard when we login adding the message function
                                        # 160 We will use the request library to direct the user to the required page by installing it with the command. "pip install requests" then we will import "request" at the top. If program did not install, try uninstalling your antivirus(i.e Smadav)
            url = request.META.get('HTTP_REFERER') # 160c Next we will comment the # 160b redirect code and write the new code for redirecting the user. But wee will first get the url from the browser and assign it to a variable(url),
            try: # 160d
                # next=/cart/checkout/
                query = requests.utils.urlparse(url).query # 160e Here we will get the next parameter and its value, assign it to a variable(query)
                # 'next' : '/cart/checkout/'
                params = dict(x.split('=') for x in query.split('&')) # 160f Here we will seperate(split using = sign) the query variable value as key : value and store it in params as dictionary(array)
                if 'next' in params: # 160g Next we will direct the user to /cart/checkout/
                    nextPage = params['next'] # 160gi
                    return redirect(nextPage) # 160gii
            except: # 160di
                return redirect('dashboard')  # 160h If the try block fail, we can direct the user to the dashboard. Next we need to see the cart items in the checkout page, So we will fix that by going to the checkout() function in the views.py # 161 file of the cart app

        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login') # 168 ends then we go to # 169 login.html to include the alert message for error
    return render(request, 'accounts/login.html') # 132 ends


# 171b We will add the login required decorator for our logout function to first check if the user is logged in else you will go to the login page.
# Now you should not be able to login a user because the 'Account model' of the models.py file of the accounts app set the user is_active = False.
# So we will send an activation link to the user, which will set the user to active, then the user can login. To send the activation email, We will 
# go to the # 172 register() function.
@login_required(login_url = 'login') # 171bii We will import the decorator at the top from dejango.contrib

# 133a create the logout function, Now we will go to the template folder and create a new folder called accounts where we will keep all the authentication files(register,login,logout)
# 133b We will now create the various files register.html and login.html and then open the register.html # 134 file.
def logout(request):
    # 171a We will write the new logout functionality after commenting the 133 own which wasnt used.
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect(login) # 171a ends

    # return render(request, 'accounts/logout.html') # 133 functionality will be commented

def activate(request, uidb64, token): # 177 We will create a simple activate function to test our email. This activation function is triggered when the user click the activation link. (passing the uidb64 and token displayed on the browser url)
    # 177c inside the function, we will now decode the userid and token, so we can set the user status to true.
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # 177ci this will decode the uidb64 and store the primary key of the user into the variable
        user = Account._default_manager.get(pk=uid) # 177cii this will return the user object, storing it in the variable.
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist): # 177ciii Here we will handle some error like type error, value error, overflow error, accoun not exist, if any of this error, we set the user to none
        user = None
    if user is not None and default_token_generator.check_token(user, token): # 177civ we will check that the user exist and that the token belong to the user
        user.is_active = True # 177cv we will set the user status to true
        user.save() # 177cvi
        messages.success(request, 'Congratulations! Your account is activated.') # 177cvii
        return redirect('login')  # 177cviii we will redirect to login if all is passed.
    else:
        messages.error(request, 'Invalid activation link') # 177cix
        return redirect('register') # 177cx
    # return HttpResponse('ok') # 117b We will import httpresponse at the top so we can display the 'OK' as a response on the webpage for now  # 177bii we will comment this and write the main function

# 184a Here we will create the function for our dashboard and the dashboard will only accessible when we login
@login_required(login_url= 'login') # 184b This login required decorator will force you to login before you can access the dashboard
def dashboard(request): # 184c
    return render(request, 'accounts/dashboard.html') # 184d So when we click on dashboard link, we will go to dashboard.php # 185 in templates/accounts

# 191 Here we will create our forgotPassword function
def forgotPassword(request):
    # 200 Here we will write the forgot password logic.
    if request.method == 'POST': # 200b We will first check if request is a POST
        email = request.POST['email'] # 200c We will take the email address from the request
        if Account.objects.filter(email=email).exists(): # 200d We check if the email entered exist in the database and then return true or false(NB: check why 'filter' is used instead of 'get')
            user = Account.objects.get(email__exact=email) # 200e We we check if the email address is exactly same as what we have in the database(NB: if we had use 'email__iexact' then the check will be case insensitive)
           
            # 200f Here we will send an reovery eamil to the user which will contain a token so that the link will automatically get expired after the reset is done.
            # First we need to first get the current site, then generate the token.
            current_site = get_current_site(request)# Here we get the current site, right now we are using localhost, but in future we will be using a domain, so we need to write our code to satisfy our future use. NB: import # 200fi current_site at the top
            mail_subject = 'Reset your account'
            message = render_to_string('accounts/reset_password_email.html', { # import 200fii render_to_string at the top
                'user': user, # We will pass the user details to the template,
                'domain': current_site, # We will pass the current_site (site domain) to the template
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)), #then pass the user primary key by encoding it so that no one will see the details of the primary key. we will decode it when we want to use it (when activating the account). NB: import # 200fiii urlsafe_base64_encode and force_bytes at the top
                'token': default_token_generator.make_token(user), # this is a default token generator which will help us create a token of the user. NB: import # 200fiv default_token_generator at the top
            }) # Here we will pass the email body(The template or text) for the email, 
            to_email = email # address to send the email ( a user email)
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # this email function take the parameter for sending an email. NB: import # 200fv EmailMessage at the top
            send_email.send() # This will send the email for us (# 200f ends). We can now create the reset_password_email.html # 201 file in the template/accounts folder and pass the message parameters to it(user,domain,uid,token)
            messages.success(request, 'Password reset email has been sent to your email address.') # 200g This will show a success message if all goes well
            return redirect('login') # 200h then we redirect to login.
        else:
            messages.error(request, 'Account does not exist!') # 200i this message will appear in the forgotPassword page if something goes wrong. We should also include the alert message in the forgotPassword.html file # 200j
            return redirect('forgotPassword') # 200k then we redirect to forgotpassword page. We can now include the forgotpassword link in login.html # 200l file in the templates/accounts
        
    # 191b next we will create the forgotPassword.html file # 192 in the teplates/accounts by copying the login.html and doing some edit
    return render(request, 'accounts/forgotPassword.html') 

# 204 Here we will create the resetpassword_validate function for taking us to the reset password page if all validation is passed. So when we click on the reset link, this function executes
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # 204a this will decode the uidb64 and store the primary key of the user into the variable
        user = Account._default_manager.get(pk=uid) # 204b this will return the user object, storing it in the variable.
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist): # 204c Here we will handle some error like type error, value error, overflow error, accoun not exist, if any of this error, we set the user to none
        user = None
    
    if user is not None and default_token_generator.check_token(user, token): # 204d Here if the token is valid, then we continue. the purpose of checking token is to whether it is a secured request or not
        request.session['uid'] = uid # 204e Next we will save the uid inside a session because we need to access the uid when resetting the password
        messages.success(request, 'Please reset your passowrd') # 204f We will create a message to display in the resetPassword.html page
        return redirect('resetPassword') # 204g This will redirect us to the resetPassword url, but first we need to go to the urls.py # 205 of the accounta app to inlude the url of the resetPassword
    else:
        messages.error(request, 'This link has expired!') # 204h A message to show if the token is invalid and user is None
        return redirect('login') # 204h We will redirect to login.html
    
# 207 Here we will crate the function for the resetPassword url we just created.
def resetPassword(request):
    if request.method == 'POST': # 212 We check if a POST was made
        password = request.POST['password'] # 213a we receive the password that was posted.
        confirm_password = request.POST['confirm_password'] # 213b we receive the confirm_password that was posted.

        if password == confirm_password: # 213c we check if the paswword equals confirm_password
            uid = request.session.get('uid')# 213d Next We will take the uid(user id) value we stored inside the session in # 204e
            user = Account.objects.get(pk=uid) # 213e We will now get the user using the uid we saved in session
            user.set_password(password) # 213f We will now use the set_password to save the password in our database. NB: If we use (save) to store the password we will get an error and it will not save. django use set_password to Hash the password before saving
            user.save() # 213g Here we save the user
            messages.success(request, 'Password reset successful') # 213h Here we create our success message
            return redirect('login') # 213i The we redirect to login page
        else: # 214a else
            messages.error(request, 'Password does not match') # 214b We display an error message if password is not same
            return redirect('resetPassword') # 214c We redirect to resetPassword.html page with the message
    else: # 212b if method is not a POST
        return render(request, 'accounts/resetPassword.html') # 212c This will take us back to the reset password template.
                                                              # 214 Next we will need to make our check-out functioality by going to the urls.py # 215 file of the carts app to add the url
    # return render(request, 'accounts/resetPassword.html') # 207b We will duplicate the login.html file and use it to create our resetPassword.html file # 208 by editing it. or we copy a fresh login.html and edit