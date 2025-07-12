
from email.mime import image
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    bio = models.CharField(max_length=900)
    experession = models.CharField(max_length=10)
    profile_pic = models.ImageField(default ="images/profile_pic.jpg",null=True, blank=True,upload_to='ecom/profile_images/')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null =True,blank =True)    
    price = models.FloatField(null= True , blank=True)
    description = models.CharField(max_length=400,null=True, blank=True)
    image = models.ImageField(null=True, blank=True,upload_to='ecom/products_images')
    digital = models.BooleanField(null=True,blank=True, default=False)
    product_sec_img1 = models.ImageField(null=True, blank=True,upload_to='ecom/products_images')
    product_sec_img2 = models.ImageField(null=True, blank=True,upload_to='ecom/products_images')
    product_sec_img3 = models.ImageField(null=True, blank=True,upload_to='ecom/products_images')
    
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    Transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id) # type: ignore
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all() # type: ignore
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping        
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() # type: ignore
        total = sum([item.get_total for item in orderitems])
        return total
        
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() # type: ignore
        total = sum([item.quantity for item in orderitems])
        return total   
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity  # type: ignore
        return total
    
class ShippingAddress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)    

class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
class Wishlist(models.Model):       
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
class Review(models.Model):     
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    review = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    digital = models.BooleanField(null=True,blank=True, default=False)
     

    def __str__(self):
        return self.name
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.product) + ' - ' + str(self.category)
class CartItem(models.Model):   
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product) + ' - ' + str(self.cart)
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product) + ' - ' + str(self.wishlist)
class ReviewItem(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product) + ' - ' + str(self.review)        
