from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
ADMIN_TYPE = 1
MENTOR_TYPE = 2
CANCIDATE_TYPE = 3
USER_TYPE_CHOICES = (
    (ADMIN_TYPE, 'admin'),
    (2, 'mentor'),
    (3, 'candidate'),
)

class TVShowUserManager(UserManager):
    def create_user(self, username, email, user_type, password=None):
        user = self.model(
             username=username,
             email=email,
             user_type=user_type
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, user_type=ADMIN_TYPE, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    objects = TVShowUserManager()

    @property
    def is_admin(self):
        return self.user_type == ADMIN_TYPE

    @property
    def is_mentor(self):
        return self.user_type == MENTOR_TYPE
    
    @property
    def is_candidate(self):
        return self.user_type == CANCIDATE_TYPE

class Team(models.Model):
    team_name = models.CharField(max_length=256)
    mentor = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @property
    def average_score(self):
        return self.performancescore_set.aggregate(models.Avg('score'))['score__avg']

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, related_name='candidates')

class Performance(models.Model):
    # Suppose that each candidate can perform multiple times
    name = models.CharField(max_length=256)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='performances')
    date = models.DateField(auto_now_add=True)

    @property
    def average_score(self):
        return self.performancescore_set.aggregate(models.Avg('score'))['score__avg']


class PerformanceScore(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])

    @classmethod
    def average_score_by_candidate(cls, candidate):
        # candidate's average score for all performance 
        return cls.objects.filter(performance__candidate=candidate).aggregate(models.Avg('score'))['score__avg']

    @classmethod
    def average_score_by_team(cls, team):
        # team's average score for all performance 
        return cls.objects.filter(performance__candidate__team=team).aggregate(models.Avg('score'))['score__avg']
