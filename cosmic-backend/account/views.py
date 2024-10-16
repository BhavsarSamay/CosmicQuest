


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import CustomUser, Token,Product,Cart
from rest_framework import status  #
from .serializers import CustomUserRegisterSerializer, CustomUserSerializer,ProductSerializer,CartSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import CustomTokenAuthentication

@api_view(['POST'])
def register_user(request):
    serializer = CustomUserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
import uuid
from datetime import datetime, timedelta
from django.utils import timezone




@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        # Fetch user based on username
        user = CustomUser.objects.get(username=username)

        # Check if the password is correct
        if check_password(password, user.password):
            # Generate a new token key
            token_key = str(uuid.uuid4())

            # Fetch the latest token for the user, if any
            token = Token.objects.filter(user=user).order_by('-created_at').first()

            if token:
                # Update the existing token
                token.key = token_key
                token.expires_at = timezone.now() + timedelta(days=7)  # Reset expiration to 7 days
                token.save()
            else:
                # Create a new token if none exists
                token = Token.objects.create(
                    user=user,
                    key=token_key,
                    expires_at=timezone.now() + timedelta(days=7)  # Set expiration to 7 days
                )

            return Response({
                'message': 'Login successful',
                'auth_token': token.key,
                'username': user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])  # Use the custom token authentication
def profile(request):
    user = request.user  # This will be set by the custom authentication class
    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_products(request):
    # Fetch all products
    products = Product.objects.all()
    
    # Serialize the product data
    serializer = ProductSerializer(products, many=True)
    
    # Return the serialized data as a JSON response
    return Response(serializer.data)

# @api_view(['POST'])
# def add_to_cart(request, username, product_id):
#     try:
#         # Assuming you have a User model linked to Cart
#         user = CustomUser.objects.get(username=username)  # Fetch the user
#         product = Product.objects.get(id=product_id)  # Fetch the product

#         # Create a cart entry
#         cart_entry = Cart(user=user, product=product)
#         cart_entry.save()  # Save the cart entry

#         # Optionally serialize the cart entry to return as a response
#         serializer = CartSerializer(cart_entry)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     except CustomUser.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def add_to_cart(request, username, product_id):
#     # Fetch the user
#     try:
#         user = CustomUser.objects.get(username=username)
#     except CustomUser.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     # Fetch the product
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

#     # Prepare data for serializer
#     cart_data = {
#         'user': user.id,  # Use user ID for foreign key reference
#         'product': product.id  # Use product ID for foreign key reference
#     }
    
#     serializer = CartSerializer(data=cart_data)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def add_to_cart(request, username, product_id):
    # Fetch the user
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Fetch the product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the product is already in the user's cart
    try:
        cart_item = Cart.objects.get(user=user, product=product)
        # If the product is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
        return Response({"message": "Product quantity increased in cart."}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        # If the product is not in the cart, add it with a quantity of 1
        cart_item = Cart.objects.create(user=user, product=product, quantity=1)
        return Response({"message": "Product added to cart.", "cart_item": CartSerializer(cart_item).data}, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# def get_user_cart(request, username):
    
#     try:
#         user = CustomUser.objects.get(username=username)  # Get the user by username
#         cart_items = Cart.objects.filter(user=user)  # Get all cart items for the user

#         serializer = CartSerializer(cart_items, many=True)  # Serialize the cart items
#         return Response(serializer.data)
#     except CustomUser.DoesNotExist:
#         return Response({"error": "User not found"}, status=404)
#     except Exception as e:
#         return Response({"error": str(e)}, status=400)
@api_view(['GET'])
def get_user_cart(request, username):
    try:
        user = CustomUser.objects.get(username=username)  # Get the user by username
        cart_items = Cart.objects.filter(user=user)  # Get all cart items for the user

        serializer = CartSerializer(cart_items, many=True)  # Serialize the cart items
        return Response(serializer.data)  # Return serialized data
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
# @api_view(['DELETE'])
# def remove_from_cart(request, username, product_id):
#     try:
#         user = CustomUser.objects.get(username=username)
#         product = Product.objects.get(id=product_id)
#         cart_item = Cart.objects.get(user=user, product=product)
#         cart_item.delete()  # Remove the item from the cart
#         return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
#     except Cart.DoesNotExist:
#         return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def remove_from_cart(request, username, product_id):
    try:
        user = CustomUser.objects.get(username=username)
        product = Product.objects.get(id=product_id)
        cart_item = Cart.objects.get(user=user, product=product)

        # Decrease quantity or remove item
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"message": "Product quantity decreased in cart."}, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
    except (CustomUser.DoesNotExist, Product.DoesNotExist, Cart.DoesNotExist):
        return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def decrease_cart_quantity(request, username, product_id):
    try:
        user = CustomUser.objects.get(username=username)
        cart_item = Cart.objects.get(user=user, product__id=product_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"message": "Quantity decreased"}, status=status.HTTP_200_OK)
        else:
            # If quantity is 1, you may want to delete it
            cart_item.delete()
            return Response({"message": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Cart.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)