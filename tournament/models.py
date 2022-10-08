from django.conf import settings

from django.db import models

from django.utils.functional import cached_property


class Role(models.Model):
    ADMIN = 'A'
    PLAYER = 'P'
    COACH = 'C'

    ROLE_TYPES = [(ADMIN, 'Admin'), (PLAYER, 'Player'), (COACH, 'Coach')]

    type = models.CharField(
        max_length=2,
        choices=ROLE_TYPES,
        default=PLAYER,
        verbose_name='Role Type'
    )

    class Meta:
        ordering = ['type']

    def __str__(self):
        return str(self.type)


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return '{first_name} {last_name} ({type})'.format(first_name=self.user.first_name,
                                                              last_name=self.user.last_name,
                                                              type=self.role.type)



class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_player',
                             on_delete=models.CASCADE)
    team = models.ForeignKey('Team', related_name='player',
                             verbose_name='Team', on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=10000,
                                 decimal_places=2,
                                 blank=True,
                                 null=False,
                                 default='0',
                                 verbose_name='Height (cm)')

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.user.first_name,
                                                 last_name=self.user.last_name)



class Coach(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_coach', on_delete=models.CASCADE)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.user.first_name,
                                                 last_name=self.user.last_name)


class Team(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=64,
        blank=False,
        null=False
    )
    coach = models.OneToOneField(
        'Coach',
        related_name='team_coach',
        verbose_name='coach',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name']

    def game_score(self, game):
        return GameTeam.objects.team(self).game(game).all()


class Game(models.Model):
    QF = 1
    SF = 2
    FI = 3
    WI = 4

    ROUNDS = [
        (QF, 'Quarter Final'),
        (SF, 'Semi Final'),
        (FI, 'Final'),
        (WI, 'Winner')
    ]

    teams = models.ManyToManyField(Team, related_name="game_team", through='GameTeam')

    date = models.DateField()

    round = models.CharField(
        max_length=2,
        choices=ROUNDS,
        default=QF
    )

    winner = models.CharField(
        verbose_name='winner',
        max_length=5,
        blank=True,
        null=True
    )


class GameTeam(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(verbose_name='score', default=0)

    class Meta:
        unique_together = ('team', 'game')

    def __str__(self):
        return '{game} {team}'.format(game=self.game.name, team=self.team.name)


class GamePlayer(models.Model):
    player = models.ForeignKey('Player', related_name='player', on_delete=models.CASCADE)

    game = models.ForeignKey('Game', related_name='game', on_delete=models.CASCADE)

    score = models.PositiveIntegerField(verbose_name='score', default=0)

    class Meta:
        unique_together = ('player', 'game',)

    def __str__(self):
        return '{player} ({game})'.format(player=self.player.full_name, game=self.game.game_name)
