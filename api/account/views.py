from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.account.serializers import UserSerializer

"""
{
    "username": "abcd123",
    "password": "1234",
    "email": "jj@naver.com"
}
"""


class UserViewSet(ViewSet):
    # 유저 생성(=회원가입)
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data)
