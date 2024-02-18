from django.db import models
from catigory.models import category
from django.urls import reverse

# Create your models here.

# 34 Here we create our store model and also import the category model as its parent model. 
# Then we go to the (admin.py # 35) file of the store app to reagister the app in the admin list
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products',)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

# 56 Here we will create a get_url fuction for the products in the home page so when we click on 
# a product name in the home page, it will take us to the product-detail page
    def get_url(self):
# 56b This takes self as an argument( called product) then a reverse(to be imported at the top) function that returns the name 
# of the path we want our page to land(product-detail.html) then we also pass two argument as a list 
# to be displayed on the page which is he category__slug and the product_slug 
# NB: (self.category.slug means product table pointing to category table (cuz category is a foreignkey to product) then pointing to category table slug). 
# Now we will go to the products page(home.html # 57) and include the get_url function to the href(link) of each product
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self) -> str:
        return self.product_name

# 111a We will create a variation manager to seperate our variations - colors from sizes, 
# then make the Variation class know that we created a variationManager 
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_active = True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active = True)
    

# 108c variation category choice dropdown(size, color)
variation_category_choice = (
    ('color', 'color'),
     ('size', 'size'),
)
# 108a We will create our variation model to be able to add a product variations(color and size) from the admin site
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # 108b We will make a dropdown of Variation categoory using the choice attribute. We will create the 
    # variation_category_choice tuple(list) above
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    #  108c is_active is use to diable any variation value
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now = True)

# 111b We will make tell the variation class that we have created a variationManager for it by instantiation a variationManager object.
# then we will go to the template( product_detail.html ) # 112 file to display our variations with the the help of the VariationManager
    objects = VariationManager()

# 108d Next we should  make migration and then migrate to create our variation model by running
# 108d python manage.py makemigrations
# 108d python manage.py migrate
# 108e Next we will go to the admin.py # 109 file of the store app to register our variation model
    def __str__(self):
        # return self.product.product_name   # used to display by product name
        return self.variation_value

