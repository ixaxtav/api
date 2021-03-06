from api.models import User, JobCoreInvite, Profile,EmployerUsers
from rest_framework import serializers
from api.serializers import employer_serializer

class OtherEmployerSerializer(serializers.ModelSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')

    class Meta:
        model = EmployerUsers
        fields = ('employer_role', 'profile_id', 'employer')


class ProfileGetSmallSerializer(serializers.ModelSerializer):
    other_employers = OtherEmployerSerializer(source='company_users_profile', many=True)
    employer = employer_serializer.EmployerGetSerializer(required=False)

    class Meta:
        model = Profile
        fields = ('picture', 'id', 'bio', 'status', 'employer', 'employer_role', 'employee', 'show_tutorial','phone_number','other_employers')



class UserGetTinySerializer(serializers.ModelSerializer):
    profile = ProfileGetSmallSerializer(many=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile')


class UserGetSmallSerializer(serializers.ModelSerializer):
    profile = ProfileGetSmallSerializer(many=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile')


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email')


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id',)
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
            'password': {'read_only': True},
            'profile': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    profile = ProfileGetSmallSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'is_active',
                  'last_name', 'email', 'password', 'profile')

    def validate(self, data):
        if 'email' in data:
            email = data["email"]
            user = User.objects.filter(email=email)
            if user.exists():
                raise ValidationError("This email is already in use.")
        elif 'username' in data:
            username = data["username"]
            user = User.objects.filter(username=username)
            if user.exists():
                raise ValidationError("This username is already in use.")
        return data

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
