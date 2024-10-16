# from django.urls import path
# from .views import register_user, login_user,profile

# urlpatterns = [
#     path('register/', register_user, name='register'),
#     path('login/', login_user, name='login'),
#     path('profile/', profile, name='profile'),   
# ]
from django.urls import path
from .views import register_user, login_user, profile,get_products,add_to_cart,get_user_cart,remove_from_cart,decrease_cart_quantity
from django.conf.urls.static import static
from django.conf import settings
app_name = 'auth'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', profile, name='profile'),
    path('products/', get_products, name='get_products'),
    path('cart/add/<str:username>/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/<str:username>/', get_user_cart, name='get_user_cart'),
    path('cart/remove/<str:username>/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/decrease/<str:username>/<int:product_id>/', decrease_cart_quantity, name='decrease_cart_quantity'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
