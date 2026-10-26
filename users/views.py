from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializer.data,
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
        # token, _ = Token.objects.get_or_create(user=user)
        # return Response(
        #     {"user": serializer.data, "token": token.key},
        #     status=status.HTTP_201_CREATED,
        # )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == "POST":
        # JWT is stateless, so logout = blacklist the refresh token
        try:
            RefreshToken(request.data["refresh"]).blacklist()
        except (KeyError, TokenError):
            return Response(
                {"error": "Valid refresh token required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_205_RESET_CONTENT)
