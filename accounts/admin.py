from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# 25 we import the Account model at the top, then register it.
# Next we will delete our existing database(db.sqlite3) and open the migration folder (not neccessary)
# in the category app and delete both created migration files(0001 and 0002) (not neccessary)
# because we dont want it any more. we want a fresh database (not neccessary)
# Now we can goto our terminal and run server (python manage.py runserver), which will give an error in the terminal, (not neccessary) 
# but we will get to create a new blank database(db.sqlite3) (not neccessary). we can now stop the server by pressing CTRL C.
# then we can now make migrations( python manage.py makemigrations) and then migrate ( python manage.py migrate) 
# which will craete our account table and category table.
# Now lets see how the admin panel looks by running server and going to the admin site. 127.0.0.1/admin
# You will see the the username input has been changed to email input because we are using the custom user model(Account)
# Recall that we dont have any superuser currently since we have deleted the database, 
# so we need to create one through our terminal by running (python manage.py createsuperuser)
# Email: webminning.space@gmail.com  Password: mynameissoL@1  we can now runserver 
# and goto the admin interface to login with this details.
# Note if it gives you an error to 'enter correct username and password' and you actually entered it correctly, 
# then you have to set its database column(is_active) to 'True' go to the project app (view.py) to see it (# 26)
# End 25

# 27 To make the password read-only and also display the account fields, we first 
# import the 'UserAdmin' class at the top, the we can now create our 'AccountAdmin' class 
# then include the AccountAdmin class in the list of registered class in # 25 code
# When you view the browser, you will see we now have our custom user model in place.

# 28 Next we will add categories from the admin interface... but before we do that, we have to configure 
# our media files same way we did for the static file in the template, so that when we upload images for 
# the categories, it will show. To do that, will will go to the project app (settings.py) # 29 file 
# and scroll down to the buttom of the file content where we do write the STATIC files code.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name','last_name','username','last_login','date_joined','is_active')
    #this makes the value of a column appear as a link to its editable page
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    #This helps make important fields like password readonly
    fieldsets = ()

# 25 code. Remove 'AccountAdmin' class and add it when you get to # 27
admin.site.register(Account, AccountAdmin)