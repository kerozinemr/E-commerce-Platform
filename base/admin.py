from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(Review)
admin.site.register(ReviewItem)
admin.site.register(ShippingAddress)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)