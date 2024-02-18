from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# 22. We will create a custom model for the superadmin(superuser)... currently, 
# we are still logging in with the username created from the terminal

class MyAccountManager(BaseUserManager):
    #22a function for creating a user(normal user)
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        # 22b normalize is used to make any email entered in capital letter to be in small letter
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        # 22c set_password is used for setting the password
        user.set_password(password)
        #this save the created user
        user.save(using=self._db)
        return user
    
    #23a function for creating the superuser
    def create_superuser(self, first_name, last_name, username, email, password):
        # 23b here we are using the create user method in 22a. it will take all the 
        # attribute from the create_superuser method and use its method(create_user method) 
        # to create the superuser and then set all the permissions required for the superuser
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        #23c this give the superuser all the permission(set to True)
        # Now goto the account model below (# 21) and instantiate the MyAccountManager class (# 23d)
        user.is_admin =True
        user_is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

# Create your models here.

# 21a. Import the 'AbstractBaseUser and BasedUserManager' then 
# Create the account model and the account manager to handle the custom user.

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # Mandatory fileds when creating custom user model
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    #I changed it to 'True' because i could'nt loggin when its value was 'False'
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    # 21b. Set the filed to login with... i.e we can login with email address instead of username
    USERNAME_FIELD = 'email'
    # 21c. Set the required fields... automatically, the email field is a required field since we will be 
    # using it to login then we need the username, first_name and last_name also
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #23d this tells the Account models that we are using the MyAccountManager class to create a user and superuser
    # Next we will go to the settings.py file of project app and tells the settings that we are going 
    # to use custom user model as # 24
    objects = MyAccountManager()

    # 21d. returns the user email when we return the account object in the template
    def __str__(self) -> str:
        return self.email
    
    # 21e. mandatory methods needed when creating custom user models
    #permmision method - if the user is admin, he has all the permission to do all the changes in the admin
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True





  