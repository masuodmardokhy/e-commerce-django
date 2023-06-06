from django.shortcuts import render, redirect, HttpResponseRedirect
#from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import *
from django.views import View
from django.shortcuts import render, get_object_or_404


# Create your views here.
class Home(View):            # for Manage the user's shopping cart information
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

    def get(self, request):
        #return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        print('aaa')
        #return HttpResponseRedirect(request,'home',)
        return render(request, 'home/home.html')


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
    return redirect('home:login')



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
        return render(request, 'home/login.html', context)


    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'home/login.html')



class Register(View):

    def get(self, request):
        return render(request, 'home/register.html')

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
        error = self.validatecustomer(customer)
        if not error:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home:home')
        else:
            data = {'error': error}
            data1 = {'value': value}
            return render(request, 'home/register.html', data, data1)

    def validatecustomer(self, custo):
        error = None
        if (not custo.first_name):
            error = "please enter first name"
        elif len(custo.first_name) <= 2:
            error = "first name must be 2 char long or more"
        elif not custo.last_name or len(custo.last_name) < 2:
            error = "please enter valid last name"
        elif not custo.phone or len(custo.phone) < 10 :
            error = "please enter valid phone "
        elif len(custo.password) < 6 :
            error = "pass must be 5 char long"
        elif len(custo.email) < 6 :
            error = "please enter valid email"
        elif custo.email.isExists():
            error = "email already register"
        return error


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')      #we can useing pop for delete data in session
        cart = request.session.get('cart')
        products = Product.products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:    #Using for, a new order is created for each product
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer), product=product, price= product.price,
                          address=address, phone= phone, quantity= cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}     #After ordering, the shopping cart will be empty
        return redirect('cart')


class OrderView(View):
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'home/order.html', {'orders':orders})



class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        product = Product.products_by_id(ids)
        print(product)
        return render(request, 'home/cart.html', {'product':product })