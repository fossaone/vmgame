import os,sys


from django.db import models
from django.contrib.auth.models import User
import django.core.exceptions

package_directory = os.path.dirname(os.path.abspath(__file__))


#Notes:
# * Need to make sure scoring is assigned to each pick

class UserProfile(models.Model):
    # This line is required.  Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    #These are additional attributes we wish to add
    country = models.CharField(max_length=100)
    score = models.PositiveIntegerField(default=0)
    created = models.DateField()
    picks = models.ManyToManyField("Pick",related_name="picks",null=True)

    def __unicode__(self):
        return u"{0} : {1}".format(self.user.username,self.score)


class Group(models.Model):
    name = models.CharField(max_length=80)
    def __unicode__(self):
        return self.name


class Scoring(models.Model):
    name = models.CharField(max_length=80)

    #Points for each selection
    group_advancer_points = models.PositiveIntegerField(default=2)
    group_perfect_points = models.PositiveIntegerField(default=5)
    qf_points = models.PositiveIntegerField(default=4)
    sf_points = models.PositiveIntegerField(default=8)
    f_points = models.PositiveIntegerField(default=16)
    third_place_points = models.PositiveIntegerField(default=16)
    champ_points = models.PositiveIntegerField(default=32)
    team_shutout_points = models.PositiveIntegerField(default=3)
    striker_goals_points = models.PositiveIntegerField(default=2)
   

class Team(models.Model):
    country = models.CharField(max_length=80)
#    abbr = models.CharField(max_length=3)
#    alt_abbr = models.CharField(max_length=2)
    group = models.ForeignKey(Group)
    group_rank = models.IntegerField(default=4)
    furthest_round = models.IntegerField(default=0)
    shutouts = models.IntegerField(default=0)
    is_third_place = models.BooleanField(default=False)
    is_champion = models.BooleanField(default=False)
    def __unicode__(self):
        #return u"{0}\n {1},\nGroup Rank {2},\nFurthest Round {3}\nShutouts {4}".format(self.country,self.group.name,self.group_rank,self.furthest_round,self.shutouts)
        return self.country


class Player(models.Model):
    name = models.CharField(max_length=80)
    team = models.ForeignKey(Team)
    position = models.CharField(max_length=80)
    goals_scored = models.IntegerField(default=0)
    def __unicode__(self):
        #return u"{0} ({1}) : {2}, Goals: {3}".format(self.name,self.position,self.team,self.goals_scored)
        #return u"{0} ({1})".format(self.name,self.team)
        return self.name


class Pick(models.Model):
    #Who's picks
    user = models.ForeignKey(UserProfile)
    #When did they pick
    pick_date = models.DateTimeField('date entered')
    pick_name = models.CharField(max_length=80)

    #Choices
    defensive_team = models.ForeignKey(Team,related_name='defensive_team')
    strikers = models.ManyToManyField(Player,related_name='strikers')
    group_winners = models.ManyToManyField(Team,related_name='group_winners')
    group_runners_up = models.ManyToManyField(Team,related_name='group_runners_up')
    group_third  = models.ManyToManyField(Team,related_name='group_third')
    group_fourth = models.ManyToManyField(Team,related_name='group_fourth')
    quarterfinal_teams = models.ManyToManyField(Team,related_name='quarterfinal_teams')
    semifinal_teams = models.ManyToManyField(Team,related_name='semifinal_teams')
    final_teams = models.ManyToManyField(Team,related_name='final_teams')
    champion = models.ForeignKey(Team,related_name='champion')
    third_place_team = models.ForeignKey(Team,related_name='third_place_team')
    total_goals = models.PositiveIntegerField(default=0)

    #Validation
    completed = models.BooleanField(default=False)

    #How many points for each selection
    scoring = models.ForeignKey(Scoring)

    #The score for this pick
    score = models.PositiveIntegerField(default=0)

    #Actual results.  May not be necessary?
    is_truth = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{0}'s pick".format(self.user)


    def validate(self):
        #Make sure choices are consistent

        #Note: defensive team and golden boot should be automatically satisfied
        ok=self.validate_strikers()
        if not ok : return ok
        ok=self.validate_group()
        if not ok : return ok
        ok=self.validate_quarters()
        if not ok : return ok
        ok=self.validate_semis()
        if not ok : return ok
        ok=self.validate_finals()
        if not ok : return ok


    def validate_strikers(self):

        num_strikers = self.strikers.objects.all().count()
        if(num_strikers != 3):
           print "error strikers"
           return False


    def validate_group(self):

        #8 Group Winners
        num_group_winners = self.group_winners.objects.all().count()
        if(num_group_winners != 8):
           print "error ngw"
           return False
        #8 Group Runners Up 
        num_group_runners_up = self.group_runners_up.objects.all().count()
        if(num_group_runners_up != 8):
           print "error ngru"
           return False

        num_group_thirds = self.group_third.objects.all().count()
        if(num_group_thirds != 8):
           print "error ngtds"
           return False

        num_group_fourths = self.group_fourth.objects.all().count()
        if(num_group_fourths != 8):
           print "error ngfts"
           return False

        #One group winner for each group
        #One group runner up for each group
        for g in Group.objects.all():
           num_group_winners = self.group_winners.objects.filter(group = g).count()
           if num_group_winners != 1: 
                print "error ngw2"
                return False
           num_group_runners_up = self.group_runners_up.objects.filter(group = g).count()
           if num_group_runners_up != 1: 
                print "error ngru2"
                return False

           num_group_thirds = self.group_third.objects.filter(group = g).count()
           if num_group_thirds != 1: 
                print "error ngtds2"
                return False

           num_group_fourths = self.group_fourth.objects.filter(group = g).count()
           if num_group_fourths != 1: 
                print "error ngfts2"
                return False
        return True


    def validate_quarters(self):
        #8 Quarterfinal teams
        num_qf_teams = self.quarterfinal_teams.objects.all().count()
        if(num_qf_teams != 8):
           print "error nqft"
           return False

        #Quarterfinal teams are from group advancers
        for qft in self.quarterfinal_teams.objects.all():
            if (qft not in self.group_winners.objects.all() or
               qft not in self.group_runners_up.objects.all()):
                print "error qft"
                return False
        return True


    def validate_semis(self):
        #4 Semifinal teams
        num_sf_teams = self.semifinal_teams.objects.all().count()
        if(num_sf_teams != 4):
           print "error nsft"
           return False

        #Semifinal teams are from quarterfinal teams
        for sft in self.semifinal_teams.objects.all():
            if sft not in self.quarterfinal_teams.objects.all():
                print "error sft"
                return False
        return True


    def validate_finals(self):
        #2 Final teams
        num_f_teams = self.final_teams.objects.all().count()
        if(num_f_teams != 4):
           print "error nft"
           return False

        #Semifinal teams are from quarterfinal teams
        for ft in self.final_teams.objects.all():
            if sft not in self.semifinal_teams.objects.all():
                print "error ft"
                return False

        #Third place is from semifinal teams
        if self.third_place_team not in self.semifinal_teams.objects.all():
            print "error tpt"
            return False

        #Champion is from final teams
        if self.champion not in self.final_teams.objects.all():
            print "error champ"
            return False
        return True


    def calculate_score(self):
        #Score the pick 
        score = 0

        #Group stage
        for gr in Group.objects.all():
            gw = self.group_winners.objects.filter(group=gr)
            if gw.group_rank < 3:
                score += self.scoring.group_advancer_points

            gru = self.group_runners_up.objects.filter(group=gr)
            if gru.group_rank < 3:
                score += self.scoring.group_advancer_points

            gt = self.group_third.objects.filter(group=gr)
            gf = self.group_fourth.objects.filter(group=gr)
            if( gw.group_rank == 1 and gru.group_rank == 2 
              and gt.group_rank == 3 and gf.group_rank == 4 ):
                score += self.scoring.group_perfect_points

        #Quarterfinals
        for qft in self.quarterfinal_teams.objects.all(): 
          if qft.furthest_round > 1:
            score += self.scoring.qf_points
 
        #Semifinals
        for sft in self.semifinal_teams.objects.all(): 
          if sft.furthest_round > 2:
            score += self.scoring.sf_points

        #Finals
        for ft in self.final_teams.objects.all(): 
          if ft.furthest_round > 3:
            score += self.scoring.f_points

        #Third-place
        if self.third_place_team.third_place == True:
          score += self.scoring.third_place_points

        #Champion
        if self.champion.champion == True:
          score += self.scoring.champ_points

        #Defensive team
        score += (self.scoring.team_shutout_points 
                   *self.defensive_team.shutouts)

        #Golden boot
        for striker in self.strikers:
          score += (self.scoring.striker_goals_points
                     *striker.goals_scored)

        self.user.score = score
        return score

def update_scores():

    try:
       #Delete any old truths
       Pick.objects.filter(is_truth=True).delete()
    except django.core.exceptions.ObjectDoesNotExist:
       pass
    #New, empty truth
    truth = Pick(is_truth=True)

    # Fill out truth based on Team and Player info
    for t in Team.objects.all():
       if team.group_rank == 1:
          truth.group_winners.add(t)
       elif team.group_rank == 2:
          truth.group_runners_up.add(t)
        
    for t in Team.objects.filter(furthest_round__gte=2):
       truth.quarterfinal_teams.add(t)

    for t in Team.objects.filter(furthest_round__gte=3):
       truth.semifinal_teams.add(t)
       
    for t in Team.objects.filter(furthest_round__gte=4):
       truth.final_teams.add(t)

    #This will fail until we set a third place
    try:
        truth.third_place_team = Team.objects.get(is_third_place=True)
    except: pass

    #This will fail until we set a champ
    try:
        truth.champion = Team.objects.get(is_champion=True)
    except: pass

    #TODO: Strikers and best defense 
    # * These are not true/untrue
    # * May want to pull the best possible picks

    #Update scores
    for e in Pick.objects.filter(is_truth=False):
        e.calculate_score()

