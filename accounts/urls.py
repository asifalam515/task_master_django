from django.urls import path,include
from accounts.views  import UserLoginView,user_logout,register,activate
urlpatterns = [
    path('register/', register,name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', user_logout,name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    


  
   
    
]