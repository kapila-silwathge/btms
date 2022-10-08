from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from tournament.models import Game
from tournament.serializers import GameSerializer


@csrf_exempt
@permission_classes([IsAuthenticated])
def list_all_games_view(request):
    user = request.user.id
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return JsonResponse({'games': serializer.data}, safe=False, status=status.HTTP_200_OK)
