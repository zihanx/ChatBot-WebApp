from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'input-field'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    
    # Customizes form validation for properties that apply to more than one field
    # Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function
        # Gets a dictionary of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username:", widget=forms.TextInput(attrs={'class': 'input-field'}))
    password  = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    confirm_password = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    
    # Customizes form validation for properties that apply to more than one field.
    # Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function
        # Gets a dictionary of cleaned data as a result
        cleaned_data = super().clean()

        # Add an extra validation
        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            # Generates a form error (non-field error)
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            # Generates a field error specific to the field (username here)
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data dictionary
        return username
    
class ChatMessageForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'new-chat-message',
            'placeholder': 'Enter a new chat message',
            'rows': 2,
            'required': True
        })
    )
    def clean_text(self):
        return self.cleaned_data["text"].strip()