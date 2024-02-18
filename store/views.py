from django.shortcuts import render, get_object_or_404
from .models import Product
from catigory.models import category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# 40 Create your views function(store) here. Then go to the template folder 
# and create a store folder with a store.html (# 41) file in the store folder.
# end # 40

# 43 We will import the Product class at the top, then query our database to get all products, 
# then use the context variable to render the products in the store.html # 44 file

# 46 We will pass the category_slug i.e shirts as a parameter to the store function to 
# query and get the products of that category
def store(request, category_slug=None):
    # 46 code
    # 46a we will import 'get_object_or_404, which will be used to get the object(categories) found
    # 46a else display the 404 error. We will also import the Category model, to be passed as a parameter in 
    # 46a the get_object_or_404() method.

    # 46b we will use the categories variable in the if statement to filter the Product model and 
    # 46b get all the products related to that category. then we want to use the category dropdown 
    # 46b in the store webpage to select a product category to display (127.0.0.1:8000/store/shirts/) 
    # 46b and we will achieve this using a python fuction called 'context processor' but we will 
    # 46b first create the file context_processor.py # 47 in the category app folder then go to the file

    categories = None
    products = None
    if category_slug != None:
        # 46c start
        # categories = get_object_or_404(category, slug=category_slug)
        # products = Product.objects.filter(category = categories, is_available = True )
        # product_count = products.count()
        # 46c end

        # 100b We will add the paginator for the product by category
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available = True )
        paginator = Paginator(products, 1) # 100b the paginator method take the object and number per page(1 objects) as parameter
        page = request.GET.get('page') # 100b this get the page number we want to display its product from the url i.e /?page=2
        paged_products = paginator.get_page(page) # 100b this store the selected object(1) in the paged_products variable
        product_count = products.count()
        # end # 100b
        # 100c Next we will go to our store.html # 101 to implement the next and previous button paginator to work with our view code
    else:
        # # 46d start
        # products = Product.objects.all().filter(is_available = True)
        # product_count = products.count()   // we commented # 46 code
        # end # 46d

        # 100a We will import the EmptyPage, PageNotAnInteger, Paginator class, so we can use the paginator to display 
        # 100a a maximum of six product per page and not all product on a page like # 46b 
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 5) # 100a the paginator method take the object and number per page(6 objects) as parameter
        page = request.GET.get('page') # 100a this get the page number we want to display its product from the url i.e /?page=2
        paged_products = paginator.get_page(page) # 100a this store the selected object(6) in the paged_products variable
        product_count = products.count()
        # end # 100a

    # 43 code
    # products = Product.objects.all().filter(is_available = True)
    # product_count = products.count()
    # end # 43
    context = {
        # 'products' : products,          // we commented # 46 context value
        'products' : paged_products,  # 100c This will send the selected objects(6) to the template
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)

# 54 We will write our function here to get a product detail and pass in the category_slug 
# and product_slug as an argument then render the result using context variable to a file called 
# product_detail.html # 55 we will create in the template/store folder
def product_detail(request, category_slug, product_slug):
    # 54b(i) We will get a single product where category_slug received as a parameter having its valus 
    # 54b(ii) from the path function in the url.py file of the store app equals the category__slug of the 
    # 54b(iii) category table slug column and product_slug received as a parameter having its value from the 
    # url.py file equals the product_slug of the product table slug column.
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)

        # 94 We want to check if the selected product in the product detail page is added to cart or not. 
        # So we will import the CartItem class at the top and also the session_id function (_cart_id) and 
        # if the CartItem filters and it exist, it will return 'True' to the in_cart variable and pass it 
        # to the context dictionary, then we will go to the product_detail.html # 95 to use the in_cart variable 
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()

    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
    }
    return render(request, 'store/product_detail.html', context)

# 103a We will write our view function to search for products.
def search(request):
    # 103c If the Keyword string is present in the GET request, we will get the value of the  keyword string
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        # 103d We will check if the keyword variable has a value, we will use it to search the database for 
        # products that has this keyword. Here we will use the Q function(import it at the top) to check 
        # if the keyword exist in the product description column OR the product title column 
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    # 103e We will then pass the result to out template using the context variable
    # 103f We will go to our template (navbar.html # 104) to implement our search url to the search bar
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)