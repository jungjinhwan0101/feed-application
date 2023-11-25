from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.account.models import User
from apps.api.account.serializers import UserSerializer, SignupApproveInputSerializer, RefreshConfirmCodeInputSerializer
from apps.account.services import AccountService


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # POST /api/users
    def create(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = AccountService.signup(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)

    # POST /api/users/signup-approve
    @action(methods=["POST"], detail=False, url_path="signup-approve")
    def approve(self, request):
        input_serializer = SignupApproveInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        username = input_serializer.validated_data['username']
        password = input_serializer.validated_data['password']
        confirm_code = input_serializer.validated_data['confirm_code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '비밀번호가 일치하지 않습니다.'})

        if user.confirm_code.code != confirm_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '인증코드가 일치하지 않습니다.'})

        if user.confirm_code.is_expired:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '인증코드가 만료되어 재발급이 필요합니다.'})

        user.active()

        return Response(status=status.HTTP_200_OK)

    # POST /api/users/refresh-confirm-code
    @action(methods=["POST"], detail=False, url_path="refresh-confirm-code")
    def refresh_confirm_code(self, request, pk):
        input_serializer = RefreshConfirmCodeInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        username = input_serializer.validated_data['username']
        password = input_serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '비밀번호가 일치하지 않습니다.'})

        AccountService.publish_confirm_code(user)

        return Response(status=status.HTTP_200_OK)
