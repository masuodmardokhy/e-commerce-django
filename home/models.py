from django.db import models
from  django.utils.timezone import datetime


class Category(models.Model):
    name = models.CharField(max_length=40)
    create = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='')

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    class Meta:
        verbose_name = 'پروفایل'



class Castomer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=60)

    def register(self):
        self.save()

    @staticmethod
    def enter_customer_by_email(getemail):
        try:
            return Castomer.objects.get(email=getemail)
        except:
            return False

    def isExists(self):
        if Castomer.objects.filter(email=self.email):
            return True
        return False



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1)
    name = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    information = models.TextField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='')

    def __str__(self):
        return self.name

    @staticmethod
    def products_by_id(id):
        return Product.objects.filter(category_id=id)

    @staticmethod
    def all_products(self):
        return Product.objects.all()

    @staticmethod
    def all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.all_products()

    def show_total_price(self):         #we have this function to discount products.
        if not self.discount:           #If there is a discount, calculate it and show the result in the total_price
            return self.unit_price
        elif self.discount:
            t = (self.unit_price * self.discount)/100
            return int(self.unit_price - t)
        return self.total_price


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Castomer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

