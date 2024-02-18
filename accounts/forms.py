from django import forms
from .models import Account

# 139a We will first import the forms, and Account model, 
# 139b Then we will create a class RegistrationForm which will inherit from the django forms. the fields in the Meta class represent the fields of the Account model. We didnt include the username field because we will create it automatically based on the email provided.
# 139c Next we will go to the view.py # 140 of the account app to modify the register view function.
class RegistrationForm(forms.ModelForm):

    # 144a We will create and modify the password and confirm password field before using them in the register template.
    # 144b In the attrs dictionary, we can provide any html attribute to modify the input field, then we will go to register.html # 145 to display the password input fields.
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        # 148 We can include the css class attribute in each input to see the proper bootstarp field like so.
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    })) # 144 ends

    # first_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder':'First Name',
    #     'class':'form-control',
    # }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    # 149 In a situation where we want to apply the bootstrap css attribue in all fields, thereby making our code short we can write:
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # 149b We add the placeholder for each field
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

        for field in self.fields:
            # 149c this loop through all the fields and assign the widget attribute(form-control) to all field
            # 149c(i) When we refresh our browser, we can now see that our bootstrap has been applied. 
            self.fields[field].widget.attrs['class'] = 'form-control'

    # 149c(ii) We will want the password field to match the forget password field by writing the code below
    # 149c(iii) Next we will want the register button to be functional, and to do that, we go to the views.py # 150 of the account app.
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
             ) # none_field_error
