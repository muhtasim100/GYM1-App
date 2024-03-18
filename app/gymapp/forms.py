from .models import CustomUser
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class RegisterUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'email', 'dob', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    
        self.fields['first_name'].widget = forms.TextInput(attrs = {'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Surname'})
        self.fields['username'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Username'})
        self.fields['email'].widget = forms.EmailInput(attrs = {'placeholder': 'Enter Email'})
        self.fields['dob'].widget = forms.DateInput(attrs = {'placeholder': 'DD-MM-YYYY', 'type': 'date'})
        # Note: Date may have problems according to Youtube. May need JS.
        self.fields['address'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Address'})
        self.fields['phone_number'].widget = forms.TextInput(attrs ={ 'placeholder': 'Enter Phone Number'})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name', 
            'last_name',
            'username',
            'email',
            'dob',
            'address',
            'phone_number',

            Submit('submit', 'Register', css_class='btn-primary')
            # Putting this here lets me reuse the same button in other forms without having to reuse code. 
            # Crispy forms feature. 
        )

     
    def allowed_username(self):
        username = self.checking['username']
        allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if not all(char in allowed_characters for char in username):
            raise ValidationError(_('Username contains invalid characters. Only letters and digits are allowed.'))
        return username