# from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# from django import forms
# from django.contrib.auth.models import User
# from .models import UserAccount

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField
#     class Meta:
#         model =User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
        
#         if commit:
#             user.save()

#             # Create UserAccount instance
#             UserAccount.objects.create(user=user)

#         return user

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserAccount

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # Additional fields from UserAccount model
    # activation_token = forms.CharField(max_length=255, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create or update UserAccount instance
            user_account, created = UserAccount.objects.get_or_create(user=user)
            # user_account.activation_token = self.cleaned_data.get('activation_token', '')
            user_account.save()

        return user
