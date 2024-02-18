from django.contrib import admin
from .models import category

# Register your models here.

# 13a. Import the category model and register it
# 14. Install the pillow package (pip install pillow [make sure internet is ON]) bcuz we are using the Image_field in the models.py file(cat_image) 
# 15. then we can make migrations
# > python manage.py makemigrations
# > python manage.py migrate
# 16. Go to admin interface(127.0.0.1/admin) on the browser and enter your login details. 
# If you dont have a login details, create one by running this(python manage.py createsuperuser)
# in the terminal window then use the details to login. Next go to models.py

# 31 Modifying the category model in the admin interface by creating a CategoryAdmin class 
# then register the CategotyAdmin class in the # 13b code. When you refresh , you will see 
# a new slug field in the category page. and when you try to add a new category(add four more category items with images),
# you can see the slug field is automatically populated. You can see all item stored in the database
# Now to see the Sqlite database, download the Sqlite Explorer extension(see your note) and open it in vs code 

# 32 Now we need to add products by creating a (store app). so in the terminal window, we type
# > python manage.py startapp store - then hit enter
# our store app will be created and we need to include it in the list of installed app in the (settings.py # 33) file
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug':('category_name',)
    }
    list_display = ('category_name', 'slug')

# 13b Registering the category model
admin.site.register(category, CategoryAdmin)
