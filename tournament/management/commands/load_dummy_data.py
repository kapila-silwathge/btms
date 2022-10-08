from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from faker import Faker

from tournament.models import Game, Role, UserRole, Player, Team, Coach, GameTeam, GamePlayer


class Command(BaseCommand):

    def roles(self, fake):
        ADMIN = 'A'
        PLAYER = 'P'
        COACH = 'C'

        ROLE_TYPES = [ADMIN, PLAYER, COACH]
        for item in range(len(ROLE_TYPES)):
            role = Role(type=ROLE_TYPES[item])
            role.save()
        self.stdout.write(self.style.SUCCESS('Successfully inserted data for Role '))

    def users(self, fake):
        for i in range(177):
            username = fake.user_name()
            password = 'kapila'
            user = User.objects.create_user(username=username + str(i), password=password, email=fake.safe_email(),
                                            first_name=fake.first_name() + str(i), last_name=fake.last_name() + str(i))
            user.save()
        self.stdout.write(self.style.SUCCESS("""Users Created. password is 'kapila'"""))

    def user_roles(self, fake):
        users = User.objects.filter(is_superuser=False)

        admin = get_object_or_404(Role, type='A')
        coach = get_object_or_404(Role, type='C')
        player = get_object_or_404(Role, type='P')

        for user in users[:160]:
            p = UserRole(user_id=user.id, role_id=player.id, is_logged_in=True)
            p.save()
        self.stdout.write(self.style.SUCCESS('User Role mapped :  %s ' % player.type))

        for user in users[160:176]:
            u = UserRole(user_id=user.id, role_id=coach.id, is_logged_in=True)

            u.save()
        self.stdout.write(self.style.SUCCESS('User Role mapped :  %s ' % coach.type))

        for user in users[176:]:
            u = UserRole(user_id=user.id, role_id=admin.id, is_logged_in=True)
            u.save()
        self.stdout.write(self.style.SUCCESS('User Role mapped :  %s ' % admin.type))

    def coaches(self, fake):
        role = get_object_or_404(Role, type='C')
        user_role = UserRole.objects.filter(role_id=role.id)

        for i in range(len(user_role)):
            coach = Coach(user_id=user_role[i].user.id)
            coach.save()
        self.stdout.write(self.style.SUCCESS('Coaches Created'))

    def teams(self, fake):
        role = get_object_or_404(Role, type='C')
        user_role = UserRole.objects.filter(role_id=role.id)

        counter = 0
        for item in range(16):
            coach = get_object_or_404(Coach, user=user_role[counter].user.id)
            team = Team(name=fake.slug(), coach=coach)
            team.save()
            counter += 1
        self.stdout.write(
            self.style.SUCCESS('Successfully inserted Teams '))

    def players(self, fake):
        teams = Team.objects.all()
        player = Role.objects.filter(type='P').first()
        users = UserRole.objects.filter(role_id=player.id)

        total = 0
        for team in teams:
            counter = 0
            while counter < 10:
                player = Player(user_id=users[total].user.id, team_id=team.id, height=fake.random_int(min=100, max=255,
                                                                                                      step=1))
                player.save()
                total += 1
                counter += 1
        self.stdout.write(self.style.SUCCESS('Players Created'))

    def qf_game(self, fake):
        teams = Team.objects.all()
        self.create_game(fake, teams, 1)

    def sf_game(self, fake):
        teams = Game.objects.filter(round=1)
        self.create_game(fake, teams, 2)

    def fi_game(self, fake):
        teams = Game.objects.filter(round=2)
        self.create_game(fake, teams, 3)

    def winner(self, fake):
        teams = Game.objects.filter(round=3)
        self.create_game(fake, teams, 4)

    def create_game(self, fake, teams, round):
        home_teams = teams[1::2]
        away_teams = teams[0::2]
        for i in range(len(home_teams)):
            home_score = fake.random_int(min=0, max=150, step=1)
            away_score = fake.random_int(min=0, max=150, step=1)
            home = home_teams[i]
            away = away_teams[i]
            winner = home if home_score > away_score else away

            game = Game(winner=winner, round=round,
                        date=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None))
            game.save()
            game_team_home = GameTeam(score=home_score, game_id=game.id, team_id=home.id)
            game_team_home.save()
            game_team_away = GameTeam(score=away_score, game_id=game.id, team_id=away.id)
            game_team_away.save()

        self.stdout.write(self.style.SUCCESS('Games with teams inserted for round  "%s" ' % round))

    def game_player(self, fake):
        game_teams = GameTeam.objects.all()

        for game_team in game_teams:
            players = Player.objects.filter(team_id=game_team.team_id)

            for i in range(len(players)):
                score = fake.random_int(min=1, max=50, step=1)

                game_player = GamePlayer(player_id=players[i].id, game_id=game_team.game_id, score=score)
                game_player.save()
        self.stdout.write(self.style.SUCCESS('Game Players inserted '))

    def handle(self, *args, **options):
        fake = Faker()
        self.stdout.write(self.style.SUCCESS('populating roles...'))
        self.roles(fake)
        self.stdout.write(self.style.SUCCESS('populating users...'))
        self.users(fake)
        self.stdout.write(self.style.SUCCESS('populating user_roles...'))
        self.user_roles(fake)
        self.stdout.write(self.style.SUCCESS('populating coaches...'))

        self.coaches(fake)
        self.stdout.write(self.style.SUCCESS('populating teams...'))
        self.teams(fake)
        self.stdout.write(self.style.SUCCESS('populating players...'))
        self.players(fake)

        self.stdout.write(self.style.SUCCESS('populating games with teams...'))
        self.qf_game(fake)
        self.sf_game(fake)
        self.fi_game(fake)
        self.winner(fake)

        self.stdout.write(self.style.SUCCESS('populating game_player...'))
        self.game_player(fake)
        self.stdout.write(self.style.SUCCESS('all completed!'))
