from django import forms
from django.contrib.auth.models import User
from vmgame.models import Pick#, UserProfile

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

class PickForm(forms.ModelForm):    
    TEAM_NAME_CHOICES = all_teams(teams)
    winner = forms.CharField(max_length=3, 
                        widget=forms.Select(choices=TEAM_NAME_CHOICES), 
                        help_text="Pick the winner of the 2014 world cup")
    GROUP_A_CHOICES = teams_in_group(teams, "A")
    groupA_winner = forms.CharField(max_length=3, 
                        widget=forms.Select(choices=GROUP_A_CHOICES), 
                        help_text="Pick the winner of group A")
    
    points = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    completed = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    
    class Meta:
            # Provide an association between the ModelForm and a model
            model = Pick
            
            fields = ('groupA_winner', "winner")
    
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