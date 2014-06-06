from django import forms
from django.contrib.auth.models import User
#from vmgame.models import Pick#, UserProfile
from vmgame.models import Team,Group,Player,Pick,UserProfile
from django.utils.translation import ugettext_lazy as _

class PickForm(forms.ModelForm): 
    def make_group_select(group_letter,rank):
           group_teams = Team.objects.filter(group__name="Group {0}".format(group_letter))
           GROUP_TEAM_CHOICES = [(t,t) for t in group_teams]
           return forms.CharField(max_length=80, 
                              widget=forms.Select(choices=GROUP_TEAM_CHOICES), 
                              help_text="Pick the {1} place team of Group {0}".format(group_letter,rank))

    groupA1st = make_group_select("A","1st");
    groupB1st = make_group_select("B","1st");
    groupC1st = make_group_select("C","1st");
    groupD1st = make_group_select("D","1st");
    groupE1st = make_group_select("E","1st");
    groupF1st = make_group_select("F","1st");
    groupG1st = make_group_select("G","1st");
    groupH1st = make_group_select("H","1st");

    groupA2nd = make_group_select("A","2nd");
    groupB2nd = make_group_select("B","2nd");
    groupC2nd = make_group_select("C","2nd");
    groupD2nd = make_group_select("D","2nd");
    groupE2nd = make_group_select("E","2nd");
    groupF2nd = make_group_select("F","2nd");
    groupG2nd = make_group_select("G","2nd");
    groupH2nd = make_group_select("H","2nd");

    groupA3rd = make_group_select("A","3rd");
    groupB3rd = make_group_select("B","3rd");
    groupC3rd = make_group_select("C","3rd");
    groupD3rd = make_group_select("D","3rd");
    groupE3rd = make_group_select("E","3rd");
    groupF3rd = make_group_select("F","3rd");
    groupG3rd = make_group_select("G","3rd");
    groupH3rd = make_group_select("H","3rd");

    groupA4th = make_group_select("A","4th");
    groupB4th = make_group_select("B","4th");
    groupC4th = make_group_select("C","4th");
    groupD4th = make_group_select("D","4th");
    groupE4th = make_group_select("E","4th");
    groupF4th = make_group_select("F","4th");
    groupG4th = make_group_select("G","4th");
    groupH4th = make_group_select("H","4th");

    class Meta:
            # Provide an association between the ModelForm and a model
            model = Pick
    
            fields = ("pick_name","champion",'third_place_team',
                      "groupA1st","groupB1st","groupC1st", "groupD1st","groupE1st","groupF1st","groupG1st","groupH1st",
                      "groupA2nd","groupB2nd","groupC2nd", "groupD2nd","groupE2nd","groupF2nd","groupG2nd","groupH2nd",
                      "groupA3rd","groupB3rd","groupC3rd", "groupD3rd","groupE3rd","groupF3rd","groupG3rd","groupH3rd",
                      "groupA4th","groupB4th","groupC4th", "groupD4th","groupE4th","groupF4th","groupG4th","groupH4th",
                      "defensive_team", 
                     )

            help_texts = {
                'pick_name': _('Provide a name for this pick.'),
                'champion': _('Pick the winner of the 2014 world cup.'),
                'third_place_team': _('Pick the team that will finish in third place.'),
                'defensive_team': _('Pick the team that will create the most shutouts.'),
            }
#            TEAM_NAME_CHOICES = [(t,t) for t in Team.objects.all()]
#            choices = {
#                'champion': TEAM_NAME_CHOICES,
#            }
            #exclude = ('user','pick_date','scoring','is_truth','points','completed')

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

