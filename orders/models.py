from django.db import models
from accounts.models import Account # 165bi Import Account model
from store.models import Product, Variation # 167bi and # 167ci import the Product and Variation model
# Create your models here.

# 265 Here we will create the model(table) for payment
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE) #265b We will import the Account model at the top
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id # 265 ends

# 266 Here we will create the model(table) for Order
class Order(models.Model):
    STATUS = {
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    }

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length = 50)
    order_note = models.CharField(max_length=50)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    # 305 Here we will write the function to concatenate the user full_name so we can call the function in the templates/orders/payment.html # 306 through the context dict "order" key
    def full_name(self):
        return f'{self.first_name} {self.last_name}' # 305 ends
    
    # 305b Here we will write the function to concatenate the user full_address so we can call the function in the templates/orders/payment.html # 306b through the context dict "order" key
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}' # 305b ends

    def __str__(self):
        return self.user.first_name # 266 ends

# 267 Here We will create the model(table) for orderProduct
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(Account, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # 267b We will import the product model
    # variation = models.ForeignKey(Variation, on_delete=models.CASCADE) # 267c We will import the Variation model
    variations = models.ManyToManyField(Variation, blank=True) # 267c (NEW CODE when we got to # 325) We will replace # 267c above with this new variation field, because of error encountered in the future at # 325. Then make migration and then migrate
    # color = models.CharField(max_length=50) # 324 We will comment the color and size field because we dont need it. we are already getting it from the variation field. then make migration by typing "python manage.py makemigration" and then migrate by typing "python manage.py migrate". 
    # size = models.CharField(max_length=50) # Next we will go back to the view.py # 325 file of the orders model, to add the ProductOrder table below the Order table and then assign value to the productorder variation.                                         
    quantity = models.IntegerField()
    product_price = models.FloatField() 
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name # 267 ends. Next we will make migration by typing "python manage.py makemigrations"
                                        # 268 Then we will run migration by typing "python manage.py migrate"
                                        # 269 Next we will want to register this three models we created in the admin.py # 270 file of the orders app
