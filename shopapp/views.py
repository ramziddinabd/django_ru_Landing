
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from .models import *
from .forms import ContactForm, CreateUserForm
from . guest_utils import *


# Create your views here.
@login_required(login_url='login')
def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == "POST" and request.POST.get('category_id'):
        category = Category.objects.all()
        products = Product.objects.filter(category=request.POST.get('category_id'))

    # elif request.method == "GET" and request.POST.get('all_products'):
    #     products = Product.objects.all()

    else:
        products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'shopapp/index.html', context)




# Views for adding Card

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home_page")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'shopapp/cart_detail.html')





# End card





def registration_user(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        form = CreateUserForm
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                return redirect('login')

        context = {'form':form}
        return render(request, 'shopapp/login.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                messages.info(request, "ERORR")
            
        context = {}

        return render(request, 'shopapp/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def cart_page(request):
    return render(request, 'shopapp/cart.html')

# def store(request):
#     data = cartData(request)
#     cartItems = data['cartItems']

#     products = Product.objects.all()
#     context = {'products': products,'cartItems': cartItems}

#     return render(request, 'shopapp/index.html', context)


# def checkout(request):
#     data = cartData(request)
#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']

#     context = {'items': items, 'order': order, 'cartItems': cartItems}
#     return render(request, 'shopapp/checkout.html', context)


# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']

#     # print('action': action)
#     # print('productId': productId)

#     customer = request.user.customer
#     product = Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)

#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


#     if action == "add":
#         orderItem.quantity = (orderItem.quantity+1)
#     elif action == "remove":
#         orderItem.quantity = (orderItem.quantity-1)

#     orderItem.save()

#     if orderItem.quantity <= 0:
#         orderItem.delete()

#     return JsonResponse('Product was added', safe=False)



# def proccessOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)

#     if request.user.is_authenticated:
#         customer = request.user.customer()
#         order, created = OrderItem.objects.get_or_create(customer=customer, complete=False)
#     else:
#         customer, order = guestOrder(request, data)


#     total = float(data['form']['total'])
#     order.transaction_id = transaction_id

#     if total == float(order.get_cart_total):
#         order.complete = True
#     order.save()

#     if order.shipping == True:
#         ShippingAddress.objects.create(
#             customer=customer,
#             order=order,
#             address=data['shipping']['address'],
#             city=data['shipping']['city'],
#             state=data['shipping']['state'],
#             postal_code=data['shipping']['postal_code'],
#         )


    






def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('name')
            return redirect('home')

    context2 = {'form':form}
    return render(request, 'shopapp/index.html', context2)
