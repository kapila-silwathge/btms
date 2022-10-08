from rest_framework import serializers

from tournament.models import Game, GameTeam, Team


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    coach = serializers.StringRelatedField()
    score = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = [
            'name',
            'coach',
            'score'
        ]


class GameTeamSerializer(serializers.ModelSerializer):
    score = serializers.StringRelatedField()
    game_id = serializers.StringRelatedField()
    team_id = serializers.StringRelatedField()

    class Meta:
        model = GameTeam
        fields = [
            'score',
            'game_id',
            'team_id',
        ]


class GameSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(read_only=True, many=True)
    date = serializers.StringRelatedField()
    round = serializers.StringRelatedField()
    winner = serializers.StringRelatedField()

    class Meta:
        model = Game
        fields = [
            'id',
            'teams',
            'round',
            'winner',
            'date',
        ]
        depth = 2
