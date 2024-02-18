from django.db import models
from store.models import Product, Variation

# Create your models here.
# 70a We will create  our cart class(model) and cartitem class(model)
# 70b We will then make migration and migrate by running: 
# 70b(i) python manage.py makemigration
# 70b(ii) python manage.py migrate
# 70c Next we will register our models(Cart, cartitem) in the admin.py # 71 file of the carts app
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank = True)
    date_added = models.DateField(auto_now_add= True)

# 70a(i) this select the field name(cart id) to display anywhere the Cart class is to be shown
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    # 70a(ii) import the product class at the top
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # 114 We will create a variation(import the Varaition class at the top) field to sore our product variations. And we will use ManyToManyField cuz many products can have same variations
    # 114b Next we will makemigrations and migrate to create our field
    # 114b python manage.py makemigration
    # 114b python manage.py migrate.
    # 114c Next we will go to the add_cart() function of the view.py # 115 file of the cart app to add our variations into the cart item
    variations = models.ManyToManyField(Variation, blank=True)
    # end # 114
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

# 80a We will create a sub_total() function to calculate the sub total of a cart item using (price and quantity) 
# 80b then refresh the cart page to see it. 
# 80c Next we will go to the cart.html # 81 file to include the add_cart() method in the plus(+) quantity button 
    def sub_total(self):
        # where self refer to the class itself(CartItem)
        return self.product.price * self.quantity

# 79a(iii) this select the field name(product) to display anywhere the Cart class is to be shown
    def __str__(self):
        return self.product.product_name
