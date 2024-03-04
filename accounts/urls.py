from django.urls import path,include
from accounts.views  import UserRegistrationView,UserLoginView,activate,user_logout
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    # path('activate/<str:uidb64>/<str:token>/', activate, name='activate_account'),
    path('logout/', user_logout,name='logout'),
    


  
   
    
]