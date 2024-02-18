# 1. import render and create a function to render our template- go to home.html
from django.shortcuts import render
from accounts.models import Account
from store.models import Product


def home(request):
    # 26 this set the superuser column (is_active) to 'True' so the superuser can login. 
    # Now refresh the template and goto the admin site to login. You can now see the admin interface
    # When we click the account model in the admin site we dont want the password field to be editable, 
    # so we goto the admin.py file of the Account model to set the password field to readonly (# 27)
    change = Account.objects.get(id = 1)
    change.is_active = 1
    change.save()
    #stop

    # 36 Import the product model and query it to get all products to be displayed in the template(index.html)
    # by passing the context variable holding the products into the render function. Now we go to the (home.html # 37)
    # to display the products.
    products = Product.objects.all().filter(is_available = True)
    context = {
        'products' : products
    }
    return render(request, 'home.html', context)