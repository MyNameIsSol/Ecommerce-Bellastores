from django.contrib import admin
from .models import Product, Variation

# Register your models here.

# 35 we import the Product model and register it, then we created a custom ProductAdmin class and 
# include it among the registered class in code # 36. Then we makemigration in the terminal window
# > python manage.py makemigrations
# > python manage.py migrate
# Next we goto our admin panel and refresh the page... you will see our new admin list (Store)
# We will now add some products by click the ( ADD PRODUCT ) button in the Product page.
# (You can add 10 products total for all categories). Next we will display this products in our 
# template through the (view.py # 36) file of the project app
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {
        'slug':('product_name',)
    }

# 36 Registers the Product class and the ProductAdmin class
admin.site.register(Product, ProductAdmin)

# 109c We will create a custom variation admin to be able to display other columns in the variation table 
# then register it with the variation class in # 109a
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    # We want to be able to filter in the variation admin page by product_name, variation_category, variation_value
    list_filter = ('product', 'variation_category', 'variation_value')

# 109a We will import the Variation model at the top, then register it so we can see our model in the admin site
# 109b When you go to the admin panel, you will see our variation model, and we will add some variation 
# (Atx Jeans, color, Red) (Atx Jeans, color, Blue) (Atx Jeans, color, Green) (Atx Jeans, size, Small) (Atx Jean, size, Medium) (Atx Jean, size, Large) so we can bring them dynamically to the template (product_detail.html) # 110
admin.site.register(Variation, VariationAdmin)