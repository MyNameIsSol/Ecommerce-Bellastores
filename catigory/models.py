from django.db import models
from django.urls import reverse

# Create your models here.

# 12. create the category model and go to the admin.py file of the category app to register it
class category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=225)
    cat_image = models.ImageField(upload_to= 'photos/categories', blank=True)

    def __str__(self) -> str:
        return self.category_name
    
# 50 We will use this custom function to return all the category slug url (links)
    def get_url(self):
        # 50b 'self' tell us we are inside the model
        # 50b We will import the reverse fuction at the top, and use it to pass the name of the 
        # 50b category slug ( products_by_category ) used in the url.py file of the store app as the path for the slug
        # 50b then we will pass the model(category) slug as an argument - self.slug( category.slug )
        # 50b The reverse function gives us the url of that particular category. Now when you click any 
        # 50b category in the dropdown of navbar.html template, you will see only the products for that category

        # 50c We will now display the category list for the store.html #51 template and make the product for 
        # 50c each categories display when selected
        return reverse('products_by_category', args=[self.slug])
    
    # 17. Add this Meta class to change the default admin categorys name to categories.
    # Then run (python manage.py makemigrations) and (python manage.py migrate)
    # 18. We will create a custom user model so we can login with email and password instead of using 
    # django builtin admin login. To do this, we will create a new app called account.
    # 19. Create an account app by running (python manage.py startapp accounts). 
    # Then go to the settings.py file(of the main project) and register the accounts app 
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

 

