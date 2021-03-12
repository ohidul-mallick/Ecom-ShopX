from django.shortcuts import render
from django.views import View
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)
from django.contrib import messages
from .forms import CustomerRegistrationform,CustomerProfileForm

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')

        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})
        
        



# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        print(product)
        return render(request,'app/productdetail.html',{'product':product})





def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')



class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()

        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city= form.cleaned_data['city']
            state= form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']

            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations !! Profile Updated succesfully..')
        return render(request,'app/profile.html',{'active':'btn-primary','form':form})



def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})



def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='SAMSUNG' or data=='REALME' or data=='APPLE':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='Below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=20000)
    elif data=='Above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=20000)

    return render(request, 'app/mobile.html',{'mobiles':mobiles})

# def login(request):
#  return render(request, 'app/login.html')




class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationform()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationform(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! You Have Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


def checkout(request):
 return render(request, 'app/checkout.html')
