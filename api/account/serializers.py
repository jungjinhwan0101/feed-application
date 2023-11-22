from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('이미 존재하는 이메일입니다.')
        return email

    def validate_password(self, password):
        if len(password) < 10:
            raise serializers.ValidationError('비밀번호는 10자 이상이어야 합니다.')

        if password.isdigit():
            raise serializers.ValidationError('숫자로만 이루워진 패스워드는 사용할 수 없습니다.')

        return password
