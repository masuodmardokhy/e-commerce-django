from django.shortcuts import render, redirect, HttpResponseRedirect
#from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import *
from django.views import View
from django.shortcuts import render, get_object_or_404


# Create your views here.
class home(View):            # for Manage the user's shopping cart information
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:                      #If the shopping cart is not empty, the number of products will be counted
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:                   #If the shopping cart is empty, a shopping cart will be created
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('home:home')

    def get(self,request):
        #return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseRedirect(request,'')



def store(request):           #this function is for show the store
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categories_id = request.GET.get('category')
    if categories_id:
        products = Product.all_products_by_categoryid(categories_id)
    else:
        products = Product.all_products()
    data = {}
    data['product'] = products
    data['categories'] = categories
    print('you are ',request.session.get('email'))
    return render(request, 'home/home.html', data)



def logout(request):
    request.session.clear()
    return redirect('')



class Login(View):
    return_url = None

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.customer_by_email(email)
        error_messages = None
        if customer:
            check_pass = check_password(password, customer.password)
            if check_pass:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('')
            else:
                error_messages = 'error'
        else:
            error_messages = 'error'
        context = {'error': error_messages}
        print(email, password)
        return render(request, '', context)


    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, '')



class Register(View):

    def get(self, request):
        return render(request, '')

    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get ('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error = None

        customer = Customer(first_name= first_name, last_name= last_name,
                            phone= phone, email= email, password= password)


