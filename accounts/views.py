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
from django.http import HttpResponse

from django.shortcuts import render

    
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('accounts/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
...



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
            
        else:    
            return render(request, 'accounts/user_registration.html')

    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/user_registration.html', {'form': form})





    


    
class UserLoginView(LoginView):
    template_name ='accounts/user_login.html'
    def get_success_url(self) :
        return reverse_lazy('home')
    
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))