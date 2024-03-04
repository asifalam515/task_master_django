from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.views.generic import FormView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth import login
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


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # User is not active until they click the activation link
#             user.save()

#             # Create UserAccount instance
#             user_account, created = UserAccount.objects.get_or_create(user=user)
#             user_account.activation_token = default_token_generator.make_token(user)
#             user_account.save()

#             # Send activation email
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your account'
#             message = render_to_string('accounts/activate_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': user_account.activation_token,
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()

#             messages.success(request, 'Check email and activate your account.')
#             return redirect('login')
#     else:
#         form = UserCreationForm()

#     return render(request, 'accounts/user_registration.html', {'form': form})



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
        return reverse_lazy('register')
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))