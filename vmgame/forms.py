from django import forms
from django.contrib.auth.models import User
#from vmgame.models import Pick#, UserProfile
from vmgame.models import Team,Group,Player,Pick,UserProfile,GROUP_LETTERS,GROUP_RANKS
from django.utils.translation import ugettext_lazy as _



class PickForm(forms.ModelForm): 

    #Striker fields
    striker1 = forms.CharField(max_length=80, 
                               widget=forms.Select(choices=[(p,p) for p in Player.objects.all()]), 
                               help_text="Pick a striker 1")
    striker2 = forms.CharField(max_length=80, 
                               widget=forms.Select(choices=[(p,p) for p in Player.objects.all()]), 
                               help_text="Pick a striker 2")
    striker3 = forms.CharField(max_length=80, 
                               widget=forms.Select(choices=[(p,p) for p in Player.objects.all()]), 
                               help_text="Pick a striker 3")

    #Some python/django kung-fu here.
    def __init__(self, *args, **kwargs):
        super(PickForm, self).__init__(*args, **kwargs)

        #Make the group fields
        for group_letter in GROUP_LETTERS:
            group_teams = Team.objects.filter(group__name="Group {0}".format(group_letter))
            GROUP_TEAM_CHOICES = [(t,t) for t in group_teams]
            for group_rank in GROUP_RANKS:
                start = ("__start" if group_rank == "1st" else "")
                end   = ("__end" if group_rank == "4th" else "")
                self.fields["sp_group{0}{1}{2}".format(group_letter,group_rank,start+end)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=GROUP_TEAM_CHOICES), 
                              help_text="Pick the finishing order of Group {0}".format(group_letter,group_rank))

        ALL_TEAM_CHOICES = [(t,t) for t in Team.objects.all()]
        #Quarterfinal teams
        
        for i in range(8):
            start = ("__start" if i==0 else "")
            br   = ("__br" if (i+1)%4==0 else "")
            self.fields["sp_qf_pick{0}{1}".format(i+1,start+br)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=ALL_TEAM_CHOICES), 
                              help_text="Pick 8 quarterfinal teams")

        #Semifinal teams
        for i in range(4):
            start = ("__start" if i==0 else "")
            end   = ("__end" if i==3 else "")
            self.fields["sp_sf_pick{0}{1}".format(i+1,start+end)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=ALL_TEAM_CHOICES), 
                              help_text="Pick 4 semifinal teams")

        #Final teams
        for i in range(2):
            start = ("__start" if i==0 else "")
            end   = ("__end" if i==1 else "")
            self.fields["sp_f_pick{0}{1}".format(i+1,start+end)] = forms.CharField(max_length=80, 
                              widget=forms.Select(choices=ALL_TEAM_CHOICES), 
                              help_text="Pick 2 final teams")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Pick

        fields = ['pick_name','third_place_team','champion','defensive_team','striker1','striker2','striker3','total_goals']
        #fields.extend(['group{0}{1}'.format(gl,gr) for gl in GROUP_LETTERS for gr in GROUP_RANKS])

        help_texts = {
            'pick_name': _('Provide a name for this pick.'),
            'champion': _('Pick the winner of the 2014 world cup.'),
            'third_place_team': _('Pick the team that will finish in third place.'),
            'defensive_team': _('Pick the team that will create the most shutouts.'),
            'total_goals': _('Enter the total number of goals that will be scored in the 2014 World Cup.'),
        }
#        exclude = ('user','pick_date','scoring','is_truth','points','completed',
#                   'group_winners','group_runners_up','group_third','group_fourth',
#                   'quarterfinal_teams','semifinal_teams','final_teams',
#                   'strikers','score',)

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

