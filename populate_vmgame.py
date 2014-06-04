import os

team_names = [
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


def populate():

    for t in team_names:
        #add_team(code=t[0], name=t[1], group=t[2])
        add_team(name=t[1], group=t[2])

def add_team(name, group, goals_against=0):
    #T = Team.objects.get_or_create(code=code, name=name, group = group, goals_against=goals_against)[0]
    T = Team.objects.get_or_create(name=name, group = group, goals_against=goals_against)[0]
    return T
        
# Start execution here!
if __name__ == '__main__':
    print "Starting VM Game population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmgame_website.settings')
    from vmgame.models import Team
    populate()