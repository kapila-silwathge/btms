# Generated by Django 3.1 on 2022-10-08 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_coach', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('round', models.CharField(choices=[(1, 'Quarter Final'), (2, 'Semi Final'), (3, 'Final'), (4, 'Winner')], default=1, max_length=2)),
                ('winner', models.CharField(blank=True, max_length=5, null=True, verbose_name='winner')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('A', 'Admin'), ('P', 'Player'), ('C', 'Coach')], default='P', max_length=2, verbose_name='Role Type')),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_logged_in', models.BooleanField(default=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('coach', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_coach', to='tournament.coach', verbose_name='coach')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.DecimalField(blank=True, decimal_places=2, default='0', max_digits=10000, verbose_name='Height (cm)')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player', to='tournament.team', verbose_name='Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_player', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__last_name', 'user__first_name'],
            },
        ),
        migrations.CreateModel(
            name='GameTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0, verbose_name='score')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.game')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.team')),
            ],
            options={
                'unique_together': {('team', 'game')},
            },
        ),
        migrations.AddField(
            model_name='game',
            name='teams',
            field=models.ManyToManyField(related_name='game_team', through='tournament.GameTeam', to='tournament.Team'),
        ),
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0, verbose_name='score')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='tournament.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player', to='tournament.player')),
            ],
            options={
                'unique_together': {('player', 'game')},
            },
        ),
    ]
