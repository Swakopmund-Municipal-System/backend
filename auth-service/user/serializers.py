from rest_framework import serializers
from django.contrib.auth import authenticate
from knox.models import AuthToken
from .models import User, UserType, UserResourcePermission

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_types', 'user_type_names', 'is_municipal_staff')

    def get_user_type_names(self, obj):
        return [ut.name for ut in obj.user_types.all()]

class UserCreateSerializer(serializers.ModelSerializer):
    user_type_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=True,
        help_text="List of user type names to assign to a new user"
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'home_address', 'user_type_names')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type_names = validated_data.pop('user_type_names')
        user = User.objects.create_user(**validated_data)

        # Add user types
        if user_type_names:
            user_types = UserType.objects.filter(name__in=user_type_names)
            user.user_types.set(user_types)

            user.is_municipal_staff = user_types.filter(is_municipal_staff=True).exists()
            User.objects.filter(pk=user.pk).update(is_municipal_staff=user.is_municipal_staff)


        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    user_type_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type_names')

    def update(self, instance, validated_data):
        user_type_names = validated_data.pop('user_type_names', None)

        instance = super().update(instance, validated_data)

        if user_type_names is not None:
            user_types = UserType.objects.filter(name__in=user_type_names)
            instance.user_types.set(user_types)

        return instance

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")



class AuthenticateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        print(user)
        if not user:
            message = ("Invalid credentials.")
            raise serializers.ValidationError(message, code='authorization')

        data['user'] = user
        return
