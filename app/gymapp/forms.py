from .models import CustomUser, WorkoutSession, Exercise
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
       
    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Field('workout_name'),
                Field('date'),
                css_class='form-row'),
            Submit('submit', 'Save', css_class='btn-primary')
        )

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'custom_name', 'reps', 'sets', 'weight']
        widgets = {
            'reps': forms.NumberInput(attrs={'placeholder': 'Enter Reps'}),
            'sets': forms.NumberInput(attrs={'placeholder': 'Enter Sets'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Enter Weight'}),
            'custom_name': forms.NumberInput(attrs={'placeholder': 'Enter Exercise Name'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('reps', css_class='form-control'),
            Field('sets', css_class='form-control'),
            Field('weight', css_class='form-control'),
            Field('custom_name', css_class='form-control'),
            Submit('submit', 'Save', css_class='btn-primary')
            )
        self.fields['name'].choices = Exercise.EXERCISE_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        custom_name = cleaned_data.get('custom_name')
        if name == 'OT' and not custom_name:
            self.add_error('custom_name', 'This field is required.')
        # If 'Other' is not selected but a custom name is entered, ignore the custom name.
        elif name != 'OT' and custom_name:
            cleaned_data['custom_name'] = ''
        return cleaned_data
