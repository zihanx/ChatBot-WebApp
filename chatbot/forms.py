from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from chatbot.models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'input-field'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    
    def clean(self):
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        return cleaned_data
    

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username:", widget=forms.TextInput(attrs={'class': 'input-field'}))
    password  = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    confirm_password = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

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

class ProfileForm(forms.ModelForm):
    current_mood_tag = forms.MultipleChoiceField(
        choices=Profile.MOOD_TAG_CHOICES,  # Use choices from model
        widget=forms.CheckboxSelectMultiple(attrs={"class": "mood-multi-select"}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ["name", "age", "gender", "bio", "interests", "current_mood_level", "current_mood_tag"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-field", "placeholder": "Enter your name"}),
            "age": forms.NumberInput(attrs={"class": "input-field", "placeholder": "Enter your age"}),
            "gender": forms.Select(attrs={"class": "input-field"}),
            "bio": forms.Textarea(attrs={"class": "input-field", "rows": 3, "placeholder": "Tell us about yourself..."}),
            "interests": forms.TextInput(attrs={"class": "input-field", "placeholder": "e.g., Music, Reading, Sports"}),
            "current_mood_level": forms.Select(attrs={"class": "input-field"}),
        }