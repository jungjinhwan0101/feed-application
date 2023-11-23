from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.account.models import User
from apps.api.account.serializers import UserSerializer
from apps.account.services import AccountService


class UserViewSet(ViewSet):
    def create(self, request) -> Response:
        return self._sign_up(request)

    def _sign_up(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = AccountService.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)
