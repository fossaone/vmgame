from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    sign_up_date = models.DateField()
    
class TeamName(models.Model):
    TEAM_NAME_CHOICES = (
        ("gre","Greece"),
        ("rus","Russia"),
        ("ned","Netherlands"),
        ("ger","Germany"),
        ("por","Portugal"),
        ("esp","Spain"),
        ("ita","Italy"),
        ("cro","Croatia"),
        ("fra","France"),
        ("eng","England"),
        ("sui","Switzerland"),
        ("bel","Belgium"),
        ("bih","Bosnia-Herzegovina"),
        ("alg","Algeria"),
        ("civ","C\u00f4te d'Ivoire"),
        ("gha","Ghana"),
        ("cmr","Cameroon"),
        ("nga","Nigeria"),
        ("mex","Mexico"),
        ("usa","United States"),
        ("hon","Honduras"),
        ("crc","Costa Rica"),
        ("arg","Argentina"),
        ("bra","Brazil"),
        ("chi","Chile"),
        ("uru","Uruguay"),
        ("col","Colombia"),
        ("ecu","Ecuador"),
        ("aus","Australia"),
        ("jpn","Japan"),
        ("kor","South Korea"),
        ("irn","Iran"),
    )
    team_name = models.CharField(max_length=3, choices=TEAM_NAME_CHOICES)
class Team(models.Model):
    
    GROUP_CHOICES = (
        ('A','Group A'),
        ('B','Group B'),
        ('C','Group C'),
        ('D','Group D'),
        ('E','Group E'),
        ('F','Group F'),
        ('G','Group G'),
        ('H','Group H'),
        )
    #code = models.CharField(max_length=3)
    team_name = models.ForeignKey(TeamName)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    goals_against = models.PositiveIntegerField(max_length=3, default=0)
     
class FinalResult(models.Model):
    TEAM_NAME_CHOICES = (
        ("gre","Greece"),
        ("rus","Russia"),
        ("ned","Netherlands"),
        ("ger","Germany"),
        ("por","Portugal"),
        ("esp","Spain"),
        ("ita","Italy"),
        ("cro","Croatia"),
        ("fra","France"),
        ("eng","England"),
        ("sui","Switzerland"),
        ("bel","Belgium"),
        ("bih","Bosnia-Herzegovina"),
        ("alg","Algeria"),
        ("civ","C\u00f4te d'Ivoire"),
        ("gha","Ghana"),
        ("cmr","Cameroon"),
        ("nga","Nigeria"),
        ("mex","Mexico"),
        ("usa","United States"),
        ("hon","Honduras"),
        ("crc","Costa Rica"),
        ("arg","Argentina"),
        ("bra","Brazil"),
        ("chi","Chile"),
        ("uru","Uruguay"),
        ("col","Colombia"),
        ("ecu","Ecuador"),
        ("aus","Australia"),
        ("jpn","Japan"),
        ("kor","South Korea"),
        ("irn","Iran"),
    )
    winner = models.CharField(max_length=3, choices=TEAM_NAME_CHOICES)
class Pick(models.Model):
    userID = models.ForeignKey(User)
    
