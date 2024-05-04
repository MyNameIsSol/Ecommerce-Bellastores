from django.urls import path # 273bi
from . import views # 273bii

# 273 import path and views file, then create a urlpattern for this urls.py file to follow, 
urlpatterns = [
  path('place_order/', views.place_order, name='place_order'), # 273biii Next we will go to the views.py # 274 file of the orders app to create the view for the orders app

  # 297 Here we will add the url to go to the payment page. Next we will go to the views.py file # 298 of the orders app to write the view function of the payment
  path('payments/', views.payments, name='payments'), 

  # 335 Here we will create the url to go to the order complete page, Next we will go to the views.py file # 336 of the orders app to write the view function of the order complete page.
  path('order_complete/', views.order_complete, name='order_complete'),
]