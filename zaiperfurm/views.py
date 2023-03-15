import uuid
from new_app.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,redirect
from .forms import *
from .models import *
import os

# Create your views here.
def index(request):
    return render(request,'index.html')

def shopreg(request):
    if request.method=='POST':
        a=shopregform(request.POST,request.FILES)
        if a.is_valid():
            un=a.cleaned_data['username']
            em= a.cleaned_data['email']
            sn= a.cleaned_data['sname']
            on= a.cleaned_data['oname']
            ps= a.cleaned_data['password']
            cps=a.cleaned_data['cpassword']
            im=a.cleaned_data['pimage']
            if ps==cps:
                b=shopregmodel(username=un,email=em,sname=sn,oname=on,password=ps,pimage=im)
                b.save()
                # return redirect()
                return redirect(shopprofile)
            else:
                return HttpResponse("Registration failed...")

    return render(request,'register.html')

def shoplogin(request):
    if request.method == 'POST':
        a = shoploginform(request.POST)
        if a.is_valid():
            un = a.cleaned_data['username']
            ps = a.cleaned_data['password']
            b = shopregmodel.objects.all()
            for i in b:

                if un == i.username and ps == i.password :
                    id=i.id
                    request.session['id']=id
                    # return redirect(f'/profile/')
                    return redirect(shopprofile)
            else:
                return HttpResponse("login failed...")
    return render(request, 'login.html')

def shopprofile(request):
    id=request.session['id']
    return render(request,'shopprofile.html',{'id':id})

def shopupload(request):
    if request.method=='POST':
        a=uploadform(request.POST,request.FILES)
        if a.is_valid():
            pn=a.cleaned_data["productname"]
            pi=a.cleaned_data["productid"]
            pr=a.cleaned_data["price"]
            di=a.cleaned_data["description"]
            im=a.cleaned_data["image"]

            b=uploadmodel(productname=pn,productid=pi,price=pr,description=di,image=im)
            b.save()
            return redirect(viewproduct)
        else:
            return HttpResponse("item failed....")
    return render(request,'shopupload.html')

def viewproduct(request):
    a=uploadmodel.objects.all()
    li=[]
    pn=[]
    pd=[]
    pr=[]
    di=[]
    id=[]
    for i in a:
        m=i.image
        li.append(str(m).split('/')[-1])
        p=i.productname
        pn.append(p)
        d=i.productid
        pd.append(d)
        r=i.price
        pr.append(r)
        f=i.description
        di.append(f)
        o=i.id
        id.append(o)
    mylist=zip(li,pn,pd,pr,di,id)
    return render(request,'viewproduct.html',{'mylist':mylist})

def shopregedit(request,id):
    a=shopregmodel.objects.get(id=id)
    if request.method=='POST':
        a.username=request.POST.get('username')
        a.email=request.POST.get('email')
        a.oname=request.POST.get('oname')
        a.password=request.POST.get('password')
        a.cpassword=request.POST.get('cpassword')
        a.pimage=request.POST.get('pimage')
        a.save()
        return HttpResponse("done")
    return render(request,'editshopreg.html',{'a':a})



def deleteproduct(request,id):
    a=uploadmodel.objects.get(id=id)
    a.delete()
    return redirect(viewproduct)

def editproduct(request,id):
    a=uploadmodel.objects.get(id=id)
    im=str(a.image).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES)>0:
            if len(a.image)>0:
                os.remove(a.image.path)
            a.image=request.FILES['image']
        a.productname=request.POST.get('productname')
        a.productid=request.POST.get('productid')
        a.price = request.POST.get('price')
        a.description=request.POST.get('description')
        a.save()
        return redirect(viewproduct)
    return render(request, 'product_edit.html', {'a': a, 'im': im})



# -----------------------------------USER-------------------------------------------------
def userregis(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if User.objects.filter(username=username).first():

            messages.success(request,'username already taken')
            return redirect(userregis)
        if User.objects.filter(email=email).first():
            messages.success(request,'email already taken')
            return redirect(userregis)
        user_obj=User(username=username,email=email)
        if password==cpassword:
            user_obj.set_password(password)
            user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email,auth_token)
        return HttpResponse("success")
    return render(request,'Userreg.html')

def send_mail_regis(email,auth_token):
    subject="your account has been verified"
    message=f'paste the link to verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(userlogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(userlogin)
    else:
        messages.success(request,"user not found")
        return redirect(userlogin)


def userlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(userlogin)
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your email')
            return redirect(userlogin)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(userlogin)
        return redirect(userprofile)
    return render(request,'Userlogin.html')

def userprofile(request):
    a=uploadmodel.objects.all()
    image=[]
    pname=[]
    pid=[]
    price=[]
    descr=[]
    for i in a:
        im=str(i.image).split('/')[-1]
        image.append(im)
        nm=i.productname
        pname.append(nm)
        prid=i.id
        pid.append(prid)
        pr=i.price
        price.append(pr)
        ds=i.description
        descr.append(ds)
    mylist=zip(image,pid,pname,price,descr)
    return render(request,'userprofile.html',{'mylist':mylist})


# ----------------------add to cart page---------
def cartdisplay(request):
    a=cartsmodel.objects.all()
    name=[]
    price=[]
    desc=[]
    image=[]
    id=[]
    for i in a:
        nm=i.cartname
        name.append(nm)
        pr=i.cartprice
        price.append(pr)
        ds=i.cartdes
        desc.append(ds)
        im=str(i.cartimage).split('/')[-1]
        image.append(im)
        id1=i.id
        id.append(id1)
    mylist=zip(id,image,name,price,desc)
    return render(request,'cart.html',{'mylist':mylist})


def addcartview(request,id):
    a=uploadmodel.objects.get(id=id)
    b=cartsmodel(cartimage=a.image,cartname=a.productname,cartprice=a.price,cartdes=a.description)
    b.save()
    return redirect(cartdisplay)

def buyproduct(request,id):
    a=cartsmodel.objects.get(id=id)
    im = str(a.cartimage).split('/')[-1]
    if request.method == 'POST':
        item_name = request.POST.get('ptname')
        item_price=request.POST.get('ptprice')
        item_quantity = request.POST.get('quantity')
        total=int(item_price)*int(item_quantity)
        return render(request,'finalbill.html',{'a':item_name,'b':item_quantity,'c':total,'d':item_price})
    pr=a.cartprice
    nm=a.cartname
    ii=a.id
    return render(request,'buyproduct.html',{'a':a,'im':im,'x':pr,'y':nm,'z':ii})
def end(request):
    return render(request,'END.html')








