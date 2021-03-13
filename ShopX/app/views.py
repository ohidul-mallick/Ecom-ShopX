from django.shortcuts import render,redirect
from django.views import View
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)
from django.contrib import messages
from .forms import CustomerRegistrationform,CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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
        item_already_in_cart=False
        if request.user.is_authenticated:

            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})




@login_required()
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_Cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempAmount=(p.quantity * p.product.discount_price)
                amount+=tempAmount
                total_amount= amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptyCart.html')


@login_required()
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempAmount=(p.quantity * p.product.discount_price)
            amount+=tempAmount
            data={
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)


@login_required()
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempAmount=(p.quantity * p.product.discount_price)
            amount+=tempAmount
            
            data={
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)

@login_required()
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempAmount=(p.quantity * p.product.discount_price)
            amount+=tempAmount

            data={
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)




@login_required()
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


@login_required()
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})


@login_required()
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orderPlaced':op})

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

@login_required()
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalAmount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempAmount=(p.quantity * p.product.discount_price)
            amount+=tempAmount
        totalAmount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'cartItems':cart_items,'totalAmount':totalAmount})

@login_required()
def paymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


