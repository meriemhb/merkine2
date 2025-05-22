from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    password = None  # On ne veut pas afficher le champ mot de passe
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                 'address', 'profile_picture', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'
        user.is_validated = True
        if commit:
            user.save()
        return user 