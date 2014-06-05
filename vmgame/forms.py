from django import forms
from django.contrib.auth.models import User
#from vmgame.models import Pick#, UserProfile
from vmgame.models import Team,Group,Player,Pick

class PickForm(forms.ModelForm):    
    TEAM_NAME_CHOICES = [(t.__unicode__(),t.__unicode__()) for t in Team.objects.all()]

    champion = forms.CharField(max_length=3, 
                        widget=forms.Select(choices=TEAM_NAME_CHOICES), 
                        help_text="Pick the winner of the 2014 world cup")
#    GROUP_A_CHOICES = teams_in_group(teams, "A")
    group_winner={}
    for group_name in ["A", "B", "C", "D", "E", "F", "G", "H"]:
       gr = Group.objects.filter(name=group_name)
       group_teams = Team.objects.filter(group=gr)
       GROUP_TEAM_CHOICES = [(t.__unicode__(),t.__unicode__()) for t in group_teams]
       #group_winner[group_name] = forms.CharField(max_length=3, 
       group_winner_test = forms.CharField(max_length=3, 
                        widget=forms.Select(choices=GROUP_TEAM_CHOICES), 
                        help_text="Pick the winner of group {0}".format(group_name))

    points = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    completed = forms.BooleanField(widget=forms.HiddenInput(), initial=False)

    class Meta:
            # Provide an association between the ModelForm and a model
            model = Pick

            #fields = ('group_winners', "champion")
            fields = ("champion","group_winner_test")

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
        fields = ('username', 'email', 'password')
        
'''class UserProfileForm(forms.ModelForm):
    #created = forms.DateField(widget=forms.HiddenInput())
    class Meta:
        model = UserProfile
        fields = ('country',)
'''
