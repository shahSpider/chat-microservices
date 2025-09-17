from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Room, RoomMembership

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

class RoomMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMembership
        fields = ('user', 'is_admin')
        
class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members_count = serializers.SerializerMethodField()
    members = RoomMembershipSerializer(source="memberships", many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'is_private', 'owner', 'members', 'members_count', 'created_at')

    def get_members_count(self, obj):
        return obj.members.count()
