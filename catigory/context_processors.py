from .models import category

# 47 the context processor takes a request as an agument and it will return a dictionary of data as a context
# Here we are using the menu_link() method to return all categories as a link

# Next we need to tell the settings.py # 48 file that we are using a context_processor by adding it 
# in the settings.py file of the project app. 
def menu_links(request):
    links = category.objects.all()
    # this brings all the categories list from the database and store them in to 
    # the links variable so that we can use the links wherever we want
    return dict(links = links)