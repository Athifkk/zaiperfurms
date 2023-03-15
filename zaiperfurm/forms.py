from django import forms

class shopregform(forms.Form):
    username=forms.CharField(max_length=20)
    email = forms.EmailField()
    sname = forms.CharField(max_length=30)
    oname = forms.CharField(max_length=20)
    password= forms.CharField(max_length=20)
    cpassword=forms.CharField(max_length=20)
    pimage=forms.ImageField()

class shoploginform(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

class uploadform(forms.Form):
    productname=forms.CharField(max_length=25)
    productid=forms.CharField(max_length=25)
    price=forms.CharField(max_length=25)
    description=forms.CharField(max_length=25)
    image=forms.ImageField()



# -----------------------------user----------------------------
class userregform(forms.Form):
    username=forms.CharField(max_length=20)
    email = forms.EmailField()
    # first_name=forms.CharField(max_length=20)
    password= forms.CharField(max_length=20)
    cpassword=forms.CharField(max_length=20)


class userlogform(forms.Form):
    username=forms.CharField(max_length=20)
    password= forms.CharField(max_length=20)
