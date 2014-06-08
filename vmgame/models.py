import os,sys,logging


from django.db import models
from django.contrib.auth.models import User
import django.core.exceptions

import vmgame

logger = logging.getLogger(__name__)

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

    def print_detail(self):
        detail_str = ""
        detail_str += "====================PICK START======================\n"
        detail_str += "User: {0}\n".format(self.user)
        detail_str += "Date: {0}\n".format(self.pick_date)
        detail_str += "Pick name: {0}\n".format(self.pick_name)

        detail_str += "Groups :\n"
        for group_letter in vmgame.GROUP_LETTERS:
            g1 = self.group_winners.get(group__name='Group {0}'.format(group_letter))
            g2 = self.group_runners_up.get(group__name='Group {0}'.format(group_letter))
            g3 = self.group_third.get(group__name='Group {0}'.format(group_letter))
            g4 = self.group_fourth.get(group__name='Group {0}'.format(group_letter))
            detail_str += "   Group {0}\n".format(group_letter)
            detail_str += "    1 : {0}\n".format(g1)
            detail_str += "    2 : {0}\n".format(g2)
            detail_str += "    3 : {0}\n".format(g3)
            detail_str += "    4 : {0}\n".format(g4)

        detail_str += "   Quarterfinal Teams:\n"
        for qft in self.quarterfinal_teams.all():
            detail_str += "    {0}\n".format(qft)

        detail_str += "   Semifinal Teams:\n"
        for sft in self.semifinal_teams.all():
            detail_str += "    {0}\n".format(sft)

        detail_str += "   Final Teams:\n"
        for ft in self.final_teams.all():
            detail_str += "    {0}\n".format(ft)

        detail_str += "   Third Place Team: {0}\n".format(self.third_place_team)
        detail_str += "   Champion: {0}\n".format(self.champion)
        detail_str += "   Defensive Team: {0}\n".format(self.defensive_team)
        detail_str += "   Strikers:\n"
        for s in self.strikers.all():
            detail_str += "    {0}\n".format(s)
        detail_str += "====================PICK STOP=======================\n"
        return detail_str

    def write_file(self):
        pick_file = "{0}-{1}".format(self.user.user.username,self.pick_date.strftime("%Y%m%d%H%M%S"))
        pick_file = os.path.join(vmgame.package_directory,'pick_records',pick_file)
        logger.info("Writing pick to file : {0}".format(pick_file))
        with open(pick_file,'w') as f:
            f.write(self.print_detail())

    def validate(self):
        #Make sure choices are consistent

        err = self.validate_groups()
        if err is not None: return err
        err = self.validate_quarters()
        if err is not None: return err
        err = self.validate_semis()
        if err is not None: return err
        err = self.validate_finals()
        if err is not None: return err
        err = self.validate_strikers()
        if err is not None: return err


    def validate_strikers(self):

        num_strikers = self.strikers.all().count()
        if(num_strikers != 3):
           return "Please choose 3 unique strikers"


    def validate_groups(self):

        #8 Group Winners
        num_group_winners = self.group_winners.all().count()
        if(num_group_winners != 8):
           return "incorrect number of group winners"
        #8 Group Runners Up 
        num_group_runners_up = self.group_runners_up.all().count()
        if(num_group_runners_up != 8):
           return "incorrect number of group runners up"

        num_group_thirds = self.group_third.all().count()
        if(num_group_thirds != 8):
           return "incorrect number of group third place teams"

        num_group_fourths = self.group_fourth.all().count()
        if(num_group_fourths != 8):
           return "incorrect number of group fourth place teams"

        #One group winner for each group
        #One group runner up for each group
        for g in Group.objects.all():
           num_group_winners = self.group_winners.filter(group = g).count()
           if num_group_winners != 1: 
                return "More than one group winner for {0}".format(g)
           num_group_runners_up = self.group_runners_up.filter(group = g).count()
           if num_group_runners_up != 1: 
                return "More than one group runner up for {0}".format(g)

           num_group_thirds = self.group_third.filter(group = g).count()
           if num_group_thirds != 1: 
                return "More than one group third place up for {0}".format(g)

           num_group_fourths = self.group_fourth.filter(group = g).count()
           if num_group_fourths != 1: 
                return "More than one group fourth place up for {0}".format(g)

           g1 = self.group_winners.get(group = g)
           g2 = self.group_runners_up.get(group = g)
           g3 = self.group_third.get(group = g)
           g4 = self.group_fourth.get(group = g)
           if (g1 == g2 or g1 == g3 or g1 == g4 or
               g2 == g3 or g2 == g4 or
               g3 == g4):
                return "Inconsistent group ranking for {0}".format(g)


    def validate_quarters(self):
        #8 Quarterfinal teams
        num_qf_teams = self.quarterfinal_teams.all().count()
        if(num_qf_teams != 8):
           return "Please choose 8 unique quarter final teams"

#TODO: Decide if we want to make sure picks are completely consistent
#        #Quarterfinal teams are from group advancers
#        for qft in self.quarterfinal_teams.all():
#            if (qft not in self.group_winners.all() or
#               qft not in self.group_runners_up.all()):
#                return "Quarterfinal team {0} not picked to advance from group".format(qft)


    def validate_semis(self):
        #4 Semifinal teams
        num_sf_teams = self.semifinal_teams.all().count()
        if(num_sf_teams != 4):
           return "Please choose 4 unique semi-final teams"

#TODO: Decide if we want to make sure picks are completely consistent
#        #Semifinal teams are from quarterfinal teams
#        #for sft in self.semifinal_teams.all():
#            if sft not in self.quarterfinal_teams.all():
#                return "Semi-final team {0} not picked to advance to quarters".format(sft)


    def validate_finals(self):
        #2 Final teams
        num_f_teams = self.final_teams.all().count()
        if(num_f_teams != 2):
           return "Please choose 2 unique final teams"

#TODO: Decide if we want to make sure picks are completely consistent
#        #Final teams are from semi-final teams
#        for ft in self.final_teams.all():
#            if ft not in self.semifinal_teams.all():
#                return "Final team {0} not picked to advance to semis".format(ft)
#
#        #Third place is from semifinal teams
#        if self.third_place_team not in self.semifinal_teams.all():
#            return "Third plac team {0} not picked to advance to semis".format(self.third_place_team)
#
#        #Champion is from final teams
#        if self.champion not in self.final_teams.all():
#                return "Champion {0} not picked to be in finals".format(self.champion)


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

