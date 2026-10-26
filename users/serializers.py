from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=8
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"error": "P1 and P2 must be same!"})

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email must be unique!"})

        account = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        account.set_password(password)
        account.save()
        self.instance = account
        return account
