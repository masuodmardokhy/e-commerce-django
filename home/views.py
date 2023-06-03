from django.shortcuts import render, redirect, HttpResponseRedirect
#from rest_framework.response import Response
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




