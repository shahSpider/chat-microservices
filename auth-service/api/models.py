from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    is_private = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='owned_rooms', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='RoomMembership', related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RoomMembership(models.Model):
    room = models.ForeignKey(Room, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')
