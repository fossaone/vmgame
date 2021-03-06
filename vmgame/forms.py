from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import vmgame
from vmgame.models import Team,Group,Player,Pick,UserProfile



class PickForm(forms.ModelForm): 

    strikers = Player.objects.filter(position="Forwards").order_by("name","team__country")
    midfielders = Player.objects.filter(position="Midfielders").order_by("name","team__country")
    defenders = Player.objects.filter(position="Defenders").order_by("name","team__country")
    keepers = Player.objects.filter(position="Goal Keepers").order_by("name","team__country")
    STRIKER_CHOICES=[(p,u"{0} ({1})".format(p,p.team.country)) for p in strikers]
    MIDFIELD_CHOICES=[(p,u"{0} ({1})".format(p,p.team.country)) for p in midfielders]
    DEFENSE_CHOICES=[(p,u"{0} ({1})".format(p,p.team.country)) for p in defenders]
    GK_CHOICES=[(p,u"{0} ({1})".format(p,p.team.country)) for p in keepers]
    PLAYER_CHOICES = (
                  ('Strikers',
                     STRIKER_CHOICES
                  ),
                  ('Midfielders',
                     MIDFIELD_CHOICES
                  ),
                  ('Defenders',
                     DEFENSE_CHOICES
                  ),
                  ('Goal Keepers',
                     GK_CHOICES
                  ),
              )
    #Striker fields
    striker1 = forms.CharField(max_length=80,
                               widget=forms.Select(choices=PLAYER_CHOICES),
                               help_text="Pick three top goal scorers")
    striker2 = forms.CharField(max_length=80,
                               widget=forms.Select(choices=PLAYER_CHOICES),
                               help_text="")
    striker3 = forms.CharField(max_length=80,
                               widget=forms.Select(choices=PLAYER_CHOICES),
                               help_text="")


    #Some python/django kung-fu here.
    def __init__(self, *args, **kwargs):
        super(PickForm, self).__init__(*args, **kwargs)

        #Make the group fields
        ALL_TEAM_CHOICES = []
        for group_letter in vmgame.GROUP_LETTERS:
            group_name = "Group {0}".format(group_letter)
            group_teams = Team.objects.filter(group__name=group_name).order_by("country")
            GROUP_TEAM_CHOICES = [ (t,t) for t in group_teams ]
            ALL_TEAM_CHOICES.extend( [ (group_name, GROUP_TEAM_CHOICES) ] )
            for i,group_rank in enumerate(vmgame.GROUP_RANKS):
                help_text = "The finishing order [1st, 2nd, 3rd, 4th] of ".format(group_name)
                help_text = (help_text if i==0 else "")
                help_text = (help_text if i!=3 else "end")
                self.fields["sp_group{0}{1}".format(group_letter,group_rank)] = (
                              forms.CharField(max_length=80, 
                              widget=forms.Select(choices=GROUP_TEAM_CHOICES), 
                              help_text=help_text))

        #Quarterfinal teams
        for i in range(8):
            help_text = "8 teams to make the quarterfinals"
            help_text = (help_text if i==0 else "")
            help_text = (help_text if i!=7 else "end")
            self.fields["sp_qf_pick{0}".format(i+1)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=ALL_TEAM_CHOICES), 
                              help_text=help_text)

        #Semifinal teams
        for i in range(4):
            help_text = "4 teams to make the semifinals"
            help_text = (help_text if i==0 else "")
            help_text = (help_text if i!=3 else "end")
            self.fields["sp_sf_pick{0}".format(i+1)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=ALL_TEAM_CHOICES), 
                              help_text=help_text)

        #Final teams
        for i in range(2):
            help_text = "2 teams to make the finals"
            help_text = (help_text if i==0 else "")
            help_text = (help_text if i!=1 else "end")
            self.fields["sp_f_pick{0}".format(i+1)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=ALL_TEAM_CHOICES),
                              help_text=help_text)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Pick

        fields = ['pick_name','third_place_team','champion','defensive_team','striker1','striker2','striker3','total_goals']

        help_texts = {
            'pick_name': _('Provide a name for this pick:'),
            'champion': _('The winner of the 2014 world cup:'),
            'third_place_team': _('The team that will finish in third place:'),
            'defensive_team': _('The team that will create the most shutouts:'),
            'total_goals': _('Enter the total number of goals that will be scored in the 2014 World Cup:'),
        }
        

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # If url is not empty and doesn't start with 'http://', prepend 'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User

        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    #created = forms.DateField(widget=forms.HiddenInput())
    class Meta:
        model = UserProfile
        fields = ('country',)

