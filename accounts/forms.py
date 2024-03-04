from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import UserAccount

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField
    class Meta:
        model =User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()

            # Create UserAccount instance
            UserAccount.objects.create(user=user)

        return user