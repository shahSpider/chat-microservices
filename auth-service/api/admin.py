from django.contrib import admin
from .models import Room, RoomMembership

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_private', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'is_admin', 'joined_at')
    search_fields = ('room__name', 'user__username')

