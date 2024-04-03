from .models import CustomUser, WorkoutSession
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    
        self.fields['first_name'].widget = forms.TextInput(attrs = {'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Surname'})
        self.fields['username'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Username'})
        self.fields['email'].widget = forms.EmailInput(attrs = {'placeholder': 'Enter Email'})
        self.fields['password1'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Password'})
        self.fields['password2'].widget = forms.TextInput(attrs = {'placeholder': 'Enter Password again'})



        self.helper = FormHelper()
        self.helper.error_text_inline = False # Error message not inline anymore.
        self.helper.layout = Layout(
            'first_name', 
            'last_name',
            'username',
            'email',
            'password1',  
            'password2', 
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



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'login'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='btn-primary')
        )

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['workout_name', 'date']
        widgets =  {
            'workout_name': forms.TextInput(attrs={'placeholder': 'Enter Workout Name'}),
            'date':forms.DateInput(attrs = {'type': 'date'}),
        }
       
    # def __init__(self, *args, **kwargs):
    #     super(WorkoutForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         'workout_name',
    #         'date',
    #         Submit('submit', 'Save', css_class='btn-primary')
    #     )
        

    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Field('workout_name'),
                Field('date'),
                css_class='form-row'),
            Submit('submit', 'Save', css_class='btn-primary')
        )