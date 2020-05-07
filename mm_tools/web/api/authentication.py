from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from mm_tools.web.models import Token
from rest_framework import exceptions


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.GET.get('token')
        if not token:
            return None

        try:
            user = Token.objects.get(token=token).user
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (user, None)
