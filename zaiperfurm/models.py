from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class shopregmodel(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    sname = models.CharField(max_length=30)
    oname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    cpassword = models.CharField(max_length=20)
    pimage = models.ImageField(upload_to="zaiperfurm/static")

class uploadmodel(models.Model):
    productname=models.CharField(max_length=25)
    productid=models.CharField(max_length=25)
    price=models.CharField(max_length=25)
    description=models.CharField(max_length=25)
    image=models.ImageField(upload_to="zaiperfurm/static")


# -------------------------------user----------------------------------------
class userregmodel(models.Model):
    username=models.CharField(max_length=20)
    email = models.EmailField()
    # first_name=models.CharField(max_length=20)
    password= models.CharField(max_length=20)
    # cpassword=models.CharField(max_length=20)


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class cartsmodel(models.Model):
    cartname=models.CharField(max_length=25)
    cartprice=models.IntegerField()
    cartdes=models.CharField(max_length=40)
    cartimage=models.ImageField(upload_to='zaiperfurm/static')



