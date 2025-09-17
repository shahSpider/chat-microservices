from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Room, RoomMembership
from .serializers import RegisterSerializer, RoomSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # List public rooms + rooms the user is a member of
        user = self.request.user
        return Room.objects.filter(Q(is_private=False) | Q(members=user)).distinct().order_by('-created_at')

    def get_object(self):
        if self.action in ['join', 'add_member']:
            return Room.objects.get(pk=self.kwargs['pk'])
        return super().get_object()
    
    def perform_create(self, serializer):
        room = serializer.save(owner=self.request.user)
        RoomMembership.objects.create(room=room, user=self.request.user, is_admin=True)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room = self.get_object()
        if room.is_private and room.owner != request.user:
            return Response({'detail': 'Room is private.'}, status=status.HTTP_403_FORBIDDEN)
        _, created = RoomMembership.objects.get_or_create(room=room, user=request.user)
        return Response({'joined': True, 'room_id': room.id}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        room = Room.objects.get(pk=pk)
        membership_status = RoomMembership.objects.create(room=room, user=self.request.user, is_admin=False)
        return Response({'room': room.name, 'membership_status': membership_status.joined_at})