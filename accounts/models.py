from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name = 'account',on_delete = models.CASCADE)
    is_active =models.BooleanField(default =False)

    
    def __str__(self) -> str:
        return self.user.first_name
