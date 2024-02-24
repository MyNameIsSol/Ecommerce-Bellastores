from django.urls import path
from . import views

# 129 We will now import 'path' and 'views', then include the url pattern list consisting of the paths to registration, login and logout.
# 129 Next will go to the urls.py # 130 our project (bellastores) and include the path to the account app
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # 182 We will create the url path for our dashboard here, thn we will go to the navbar.html # 183 in templates/includes to add the link
    path('dashboard/', views.dashboard, name='dashboard'),
    # 190 We want that in the url, if we just have it like this domain.com/accounts/ instead of domain.com/accounts/dashboard it should still take us to dashboard and not (page not found). so we do this
    path('', views.dashboard, name='dashboard'), # 190b Next we will begin the forgot password path. To do this we will create is url below.

    # 176 We will create the 'activate' link used in the account_verification_email here
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), # 176b Then we will goto # 177 views.py file of the account app and create an activate function 

    # 190c We will create the url for forgot password here
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'), # Next we will go to the views.py # 191 of the account app to create a forgotPassword function.

    # 203 Here we will create our resetpassword_validate url then goto the views.py # 204 file of the account app to create the function.
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),

    # 205 Here we will create our resetpassword url for the resetPassword.html page
    path('resetPassword/', views.resetPassword, name='resetPassword'), # 206 Next we will go to the views.py file # 207 of the accounts app to make the views for the resetPassword url


]