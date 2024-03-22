from .models import CustomUser
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'email', 'dob', 'address', 'phone_number']
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    
        self.fields['first_name'].widget = forms.TextInput(attrs = {'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Surname'})
        self.fields['username'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Username'})
        self.fields['email'].widget = forms.EmailInput(attrs = {'placeholder': 'Enter Email'})
        self.fields['dob'].widget = forms.DateInput(attrs = {'placeholder': 'DD-MM-YYYY', 'type': 'date', 'class': 'form-control'})
        # Note: Date may have problems on some browsers according to Youtube. May need JS.
        self.fields['address'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Address'})
        self.fields['phone_number'].widget = forms.TextInput(attrs ={ 'placeholder': 'Enter Phone Number'})

        self.helper = FormHelper()
        self.helper.error_text_inline = False # Error message not inline anymore.
        self.helper.layout = Layout(
            'first_name', 
            'last_name',
            'username',
            'email',
            'dob',
            'address',
            'phone_number',

            Submit('submit', 'Sign Up', css_class='btn-primary')
            # Putting this here lets me reuse the same button in other forms without having to reuse code. 
            # Crispy forms feature. 
        )

    # Django has a clean_username method so by defining my own one I can customize the error message.
    def clean_username(self): 
        username = self.cleaned_data['username']
        if not username.isalnum():
            raise ValidationError(_('Username contains invalid characters.\n Only letters and digits are allowed.'))
        return username
    # Making sure username is only numbers and letters.



class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',

            Submit('submit', 'Login', css_class='btn-primary')
        )