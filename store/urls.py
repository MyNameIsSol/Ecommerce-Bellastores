from django.urls import path
from . import views

# 38 import path and views file, then create a urlpattern for the urls.py file to follow, 
# then go to the urls.py # 39 file of the project app to include the store urls.py file to be recognized by our project
urlpatterns = [
    path('', views.store, name='store'),

# 45 We will add a url pattern to match the category selected in the store webpage(store.html). 
# i.e if we have a url like '127.0.0.1:8000/store/category_slug(shirts)' we should see all the products in the shirt category
# /shirts/ becomes the slug to be passed to the url. so we will go to the view.py # 46 file 
# to use the category_slug i.e shirt to get the products
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),

# 53 We will add the url pattern to go to the product detail page when a product is selected in the store app, 
# then we will go to the views.py # 54 file of the store app and write the product_detail fuction
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
         
# 102 We will add the url pattern to search for a product using the search bar then we will go to the 
# view.py # 103 file to create the view function
    path('search/', views.search, name='search'),
]