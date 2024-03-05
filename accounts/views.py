from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.views.generic import FormView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,get_user_model
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import CreateView
from .tokens import account_activation_token
from django.http import HttpResponse
from .forms import UserRegistrationForm
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login

    
def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Thanks you for your email confirmation.You can login here ")
    else:
        messages.error(request,"Activate link is Invalid")   
    return redirect('home')

def activateEmail(request,user,to_email):
    mail_subject = "Activate Your user Account"
    message = render_to_string("accounts/template_activate_account.html",
    {
        'user':user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
            'protocol':'https' if request.is_secure() else 'http'
        
    }
 )
    email = EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
        messages.success(request,f"Dear {user},Please go to your email <b> {to_email} </b> inbox and click to the activation link ")
    else:
        message.error(request,f'problem to sending your email')

from django.http import HttpResponse

from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activateEmail(request, user, form.cleaned_data.get('email'))
            
            # Render a success page or redirect to a success URL
            return render(request, 'accounts/user_registration.html')

    else:
        form = UserRegistrationForm()

    # Render the registration form again with validation errors
    return render(request, 'accounts/user_registration.html', {'form': form})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_account = UserAccount.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, UserAccount.DoesNotExist):
        user = None

    if user is not None and user_account is not None and default_token_generator.check_token(user, token):
        user_account.is_active = True
        user_account.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('register')

    




    
class UserLoginView(LoginView):
    template_name ='accounts/user_login.html'
    def get_success_url(self) :
        return reverse_lazy('home')
    
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))