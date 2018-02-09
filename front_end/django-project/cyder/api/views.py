from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

@api_view()
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def token_from_session(request):
    (token, _) = Token.objects.get_or_create(user=request.user)
    return Response({ "token": token.key })
