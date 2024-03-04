from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.views.generic import FormView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.urls import reverse_lazy
import secrets







# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url =reverse_lazy('home')
    def form_valid(self, form):
        # print(form.cleaned_data)
        user = form.save() 
        login(self.request,user)
        print(user)
        return super().form_valid(form) 




    
    
    
class UserLoginView(LoginView):
    template_name ='accounts/user_login.html'
    def get_success_url(self) :
        return reverse_lazy('register')
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))