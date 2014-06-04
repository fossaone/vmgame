from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

teams = [
    ("gre","Greece","C"),
    ("rus","Russia","H"),
    ("ned","Netherlands","B"),
    ("ger","Germany","G"),
    ("por","Portugal","G"),
    ("esp","Spain","B"),
    ("ita","Italy","D"),
    ("cro","Croatia","A"),
    ("fra","France","E"),
    ("eng","England","D"),
    ("sui","Switzerland","E"),
    ("bel","Belgium","H"),
    ("bih","Bosnia-Herzegovina","F"),
    ("alg","Algeria","H"),
    ("civ","Cote d'Ivoire","C"),
    ("gha","Ghana","G"),
    ("cmr","Cameroon","A"),
    ("nga","Nigeria","F"),
    ("mex","Mexico","A"),
    ("usa","United States","G"),
    ("hon","Honduras","E"),
    ("crc","Costa Rica","D"),
    ("arg","Argentina","F"),
    ("bra","Brazil","A"),
    ("chi","Chile","B"),
    ("uru","Uruguay","D"),
    ("col","Colombia","C"),
    ("ecu","Ecuador","E"),
    ("aus","Australia","B"),
    ("jpn","Japan","C"),
    ("kor","South Korea","H"),
    ("irn","Iran","F"),
]

def teams_in_group(teams, group1, group2=None, group3=None, group4=None):
    team_choices = []
    for t in teams:
        if t[2]==group1 or t[2]==group2 or t[2]==group3 or t[2]==group4:
            team_choices.append(t[0:2])
    return team_choices
    
    
def all_teams(teams):
    team_choices = []
    for t in teams:
        team_choices.append(t[0:2])
    return team_choices
    
GROUP_CHOICES = [
    ('A','Group A'),
    ('B','Group B'),
    ('C','Group C'),
    ('D','Group D'),
    ('E','Group E'),
    ('F','Group F'),
    ('G','Group G'),
    ('H','Group H'),
]

'''
class UserProfile(models.Model):
    # This line is required.  Links UserProfile to a User model instance.
    #username = models.CharField(max_length=40, unique=True)
    #USERNAME_FIELD = 'username'
    #These are additional attributes we wish to add
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    country = models.CharField(max_length=50)
    #REQUIRED_FIELDS = ['country',]
    
    def __unicode__(self):
        return self.user.username
'''    
        
class Team(models.Model):
    #code = models.CharField(max_length=3)
    #name = models.CharField(max_length=100)
    TEAM_NAME_CHOICES = all_teams(teams)
    name = models.CharField(max_length=3, choices=TEAM_NAME_CHOICES)
    #code = models.CharField(max_length=3)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    goals_against = models.PositiveIntegerField(max_length=3, default=0)
    
    def __unicode__(self):
        return self.name
    
     
'''class FinalResult(models.Model):
    winner = models.CharField(max_length=3)
    points = models.PositiveIntegerField(max_length=3, default=0)
    round = models.PositiveIntegerField(max_length=2, default=0)
    
    def __unicode__(self):
        return self.round
'''
    
class Pick(models.Model):
    #user = models.ForeignKey(User)
    #name = models.CharField(max_length=30, unique=True)
    TEAM_NAME_CHOICES = all_teams(teams)
    GROUP_A_CHOICES = teams_in_group(teams, "A")
    winner = models.CharField(max_length=3, choices=TEAM_NAME_CHOICES)
    groupA_winner = models.CharField(max_length=3, choices=GROUP_A_CHOICES)
    points = models.PositiveIntegerField(max_length=3, default=0)
    completed = models.BooleanField(default=False)
    
    #def __unicode__(self):
        #return self.user
        
class Player(models.Model):
    name = models.CharField(max_length=3)
    team = models.CharField(max_length=100)
    goals = models.PositiveIntegerField(max_length=2, default=0)
    
    def __unicode__(self):
        return self.name
    