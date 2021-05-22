from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    
class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    content = models.TextField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="photos/%Y%m%d")
    created_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name 



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_items = self.order_items_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_sum(self):
        order_items = self.order_items_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.order_items_set.all()
        total = sum([item.quantity for item in order_items])
        return total




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name

    
