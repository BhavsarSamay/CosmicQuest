from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the request's 'Authorization' header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Split "Token <token_key>"
        try:
            token_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Invalid token header. No token provided.')

        # Check if the token exists and is valid
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        # Check if the token has expired
        if not token.is_valid():
            raise AuthenticationFailed('Token has expired.')

        # Return the associated user and token
        return (token.user, token)

