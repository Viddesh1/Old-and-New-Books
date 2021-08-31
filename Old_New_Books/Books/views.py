from django import forms
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext
from django.views import View
from . models import Customer, Product, OrderPlaced, Cart, Feedback
from . forms import CustomerRegistrationForm, CustomerProfileForm, FeedbackForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay

# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        newbooks = Product.objects.filter(category='N')
        oldbooks = Product.objects.filter(category='O')
        # mobiles = Product.objects.filter(category='M')
        # laptops = Product.objects.filter(category="L")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'newbooks': newbooks, 'oldbooks': oldbooks, 'totalitem':totalitem})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

@method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            feedback_data = Feedback.objects.filter(product = pk)  # Q() & Q() # Feedback.objects.all() 
        return render(request, 'app/productdetail.html', {"form": feedback_data, "product":product, "item_already_in_cart": item_already_in_cart, 'totalitem':totalitem})
    def post(self, request, pk):                # "form": feedback_data,
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        form = FeedbackForm(request.POST)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        if form.is_valid():
            user_feedback = form.cleaned_data['feedback']
            product_id = Product.objects.get(id=pk)
            username = Customer.objects.filter(user = request.user).first()
            messages.success(request, 'Thank you for your feedback')
            try:
                Feedback(feedback = user_feedback, product = product_id, username=username).save() # product = product_id
            except:
                return redirect('/profile')
        # return render(request, 'app/productdetails.html', {'form':form, "product":product, "item_already_in_cart": item_already_in_cart, 'totalitem':totalitem})
        return redirect('/product-detail/' + str(pk))


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        carts = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                return render(request, 'app/addtocart.html', {'carts': carts, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount

            data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        totalamount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
        data = {
            'amount': amount,
            'totalamount': totalamount
            }
        return JsonResponse(data)

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    orderplaced = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':orderplaced, 'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')


def oldbooks(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        old_books = Product.objects.filter(category='O')
    elif data == 'Author1' or data == 'Author2' or data == 'Author3':
        old_books = Product.objects.filter(category='O').filter(author = data)
    elif data == 'Action_and_Adventure':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'AA')
    elif data == 'Classics':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'C')
    elif data == 'Comic_Book_or_Graphic_Novel':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'CG')
    elif data == 'Detective_and_Mystery':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'DM')
    elif data == 'Fantasy':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'F')
    elif data == 'Historical_Fiction':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'HF')
    elif data == 'Horror':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'H')
    elif data == 'Literary_Fiction':
        old_books = Product.objects.filter(category='O').filter(sub_category = 'LF')
    elif data == 'Below':
        old_books = Product.objects.filter(category='O').filter(discounted_price__lt = 400)
    elif data == 'Above':
        old_books = Product.objects.filter(category='O').filter(discounted_price__gt = 400)
    return render(request, 'app/old_books.html', {'oldbooks': old_books, 'totalitem':totalitem})


def newbooks(request, data=None):
    if data == None:
        new_books = Product.objects.filter(category='N')
    elif data == 'newAuthor1' or data == 'newAuthor2' or data == 'newAuthor3':
        new_books = Product.objects.filter(category='N').filter(author = data)
    elif data == 'Action_and_Adventure':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'AA')
    elif data == 'Classics':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'C')
    elif data == 'Comic_Book_or_Graphic_Novel':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'CG')
    elif data == 'Detective_and_Mystery':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'DM')
    elif data == 'Fantasy':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'F')
    elif data == 'Historical_Fiction':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'HF')
    elif data == 'Horror':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'H')
    elif data == 'Literary_Fiction':
        new_books = Product.objects.filter(category='N').filter(sub_category = 'LF')
    elif data == 'Below': 
        new_books = Product.objects.filter(category='N').filter(discounted_price__lt = 900)
    elif data == 'Above':
        new_books = Product.objects.filter(category='N').filter(discounted_price__gt= 900)
    return render(request, 'app/new_books.html', {'newbooks': new_books})


# def buttomwear(request, data=None):
#     if data == None:
#         buttomwear = Product.objects.filter(category='BW')
#     elif data == 'Aachho' or data == 'Reebok' or data == 'Adidas':
#         buttomwear = Product.objects.filter(category='BW').filter(brand = data)
#     elif data == 'Below':
#         buttomwear = Product.objects.filter(category='BW').filter(discounted_price__lt = 1000)
#     elif data == 'Above':
#         buttomwear = Product.objects.filter(category='BW').filter(discounted_price__gt = 1000)
#     return render(request, 'app/buttomwear.html', {'buttomwear': buttomwear})

# def laptop(request, data=None):
#     if data == None:
#         laptop = Product.objects.filter(category='L')
#     elif data == 'Apple' or data == 'Alienware' or data == 'Asus':
#         laptop = Product.objects.filter(category='L').filter(brand = data)
#     elif data == 'Below':
#         laptop = Product.objects.filter(category='L').filter(discounted_price__lt = 1000)
#     elif data == 'Above':
#         laptop = Product.objects.filter(category='L').filter(discounted_price__gt = 1000)
#     return render(request, 'app/laptop.html', {'laptop': laptop})


def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Account Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    totalamount2 = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
        totalamount2 = int(totalamount) * 100
        print("Total Amount is: ", totalamount)
        print("Total2 Amount2 is:", totalamount2)
    return render(request, 'app/checkout.html', {'add': address, 'totalamount2': totalamount2, 'totalamount': totalamount, 'cart_item':cart_item, 'totalitem':totalitem})

@login_required
def payment_done(request):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    custid = request.GET.get('custid')
    if custid == None:
        messages.info(request, "Please select any one Address")
        return redirect("checkout")
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            amount = 50000

            client = razorpay.Client(
                auth=("rzp_test_qTtvD3GKTTNxSr", "q3ShZ5AhDO2pgOKctYcMA2Jj"))

            payment = client.order.create({'amount': amount, 'currency': 'INR',
                                        'payment_capture': '1'})
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totalitem = 0
    def get(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem':totalitem})
    
    def post(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Your profile is updated successfully')
        return render(request, 'app/profile.html', {'form': form, 'active':'btn-primary', 'totalitem':totalitem})


class FeedbackView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            form = FeedbackForm()
        return render(request, 'app/feedback.html', {'pk': pk, "form": form, "product":product, "item_already_in_cart": item_already_in_cart, 'totalitem':totalitem})
    # def post(self, request, pk):
    #     form = FeedbackForm(request.POST)
    #     if form.is_valid():
    #         user_feedback = form.cleaned_data['feedback']
    #         product_id = pk
    #         messages.success(request, 'Congratulations! Books Sold Successfully')
    #         form.save(feedback = user_feedback, product = product_id, commit=False)
    #     return render(request, 'app/productdetails.html', {'form':form})

# def sell(request):
#     if request.user.is_authenticated:
#         pass

# @method_decorator(login_required, name='dispatch')
# class SellView(View):
#     def post(self, request):
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             messages.success(request, 'Congratulations! Books Sold Successfully')
#             form.save()
#         return render(request, 'app/productdetails.html', {'form':form})


def contactus(request):
    return render(request, 'app/contactus.html')

def aboutus(request):
    return render(request, 'app/aboutus.html')