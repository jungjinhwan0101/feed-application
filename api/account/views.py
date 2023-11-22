from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from account.models import User
from api.account.serializers import UserSerializer


class UserViewSet(ViewSet):
    def create(self, request):
        return self._sign_up(request)

    def _sign_up(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(username=serializer.validated_data['username'],
                                        email=serializer.validated_data['email'],
                                        password=serializer.validated_data['password'])

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)
