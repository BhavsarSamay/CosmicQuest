from django.contrib import admin
from .models import CustomUser ,Token,Product,Cart
# Register your models here.    
admin.site.register(CustomUser)
admin.site.register(Token)
admin.site.register(Product)
admin.site.register(Cart)