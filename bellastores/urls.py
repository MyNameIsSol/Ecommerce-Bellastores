"""bellastores URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 4. Import the view file and add the render function(home()) to path- then add static folder in (PROJRECT APP) - goto settings.py(buttom page)
from . import views

# 30a importation of static and settings
from django.conf.urls.static import static
from django.conf import settings
# end # 30a

urlpatterns = [
    path('admin/', admin.site.urls),
         
# 4 add render function for home to path
    path('', views.home, name='home'),
         
# 39 import the include function at the top to include the store app urls.py file, 
# then go to the views.py # 40 file of the store app to create a view function(store)
    path('store/', include('store.urls')),
                           
# 66 Here we will add the path to the cart app so when we have a url like 127.0.0.1:8000/cart/ 
# it will take us to the url.py # 67 file of the carts app
    path('cart/', include('carts.urls')),

# 130 Here we will include the path to the account app and then go to the views.py # 131 file of the account app to create the various view functions.
    path('accounts/', include('accounts.urls')),

# 271 Here we will create our url pattern for the placeOrder button in the checkout template. 
    path('orders/', include('orders.urls')), # 272 Next we will create a urls.py # 273 file in the orders app 

# 30b import (static) and (settings) then add static function to urlpattern using the + sign 
# Next we can go to the category list to add some categories by clicking the ADD CATEGORY button.
# When you add a category item (just one item for now) including its image, you click on save. you will see a successful message.
# To be sure the category image is well added, click on the added category to display its editable page, 
# then you click on the image link of the category image field.
# Next we will modify the category slug field in the (admin.py # 31) file of the category app, 
# so that whenever we add a category_name, the slug will be auto populated in the admin interface
# end # 30
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
