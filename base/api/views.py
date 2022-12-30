from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Group
from .serializers import GroupSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Group.objects.all()
    serializer = GroupSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, id):
    room = Group.objects.get(id=id)
    serializer = GroupSerializer(room, many=False)
    return Response(serializer.data)
