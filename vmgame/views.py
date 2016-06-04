#python lib
import datetime
import logging

#django
from django.shortcuts import render_to_response
#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
import django.core.exceptions
import django

#vmgame
import vmgame
from vmgame.models import (Team, Player, Group, User, Scoring,
                           UserProfile, Pick, Event)
from vmgame.forms import PickForm, UserForm, UserProfileForm

logger = logging.getLogger(__name__)

#global_context_dict is at file scope to have some app level info
global_context_dict = {}
global_context_dict['tournament_started'] = vmgame.config.TOURNAMENT_START < datetime.datetime.utcnow()

def register(request):
    logger.info('in register view')
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was succesful.
    # Set to False initially.  Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab info from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.created = datetime.datetime.now()

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable and tell the template registration was succesful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to teh terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #{'user_form': user_form, 'registered': registered}
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    context_dict.update(global_context_dict)
    # Render the template depending on the context.
    return render_to_response('emgame/register.html', context_dict, context)


def user_login(request):
    # obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's  machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a user object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can Log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/emgame/')
            else:
                # An inactive account was used - no Logging in!
                return HttpResponse("Your VM Game account is disabled.")
        else:
            # Bad Login details were provided.  So we can't Log the user in.
            print " Invalid login details: {0}, {1}".format(username,password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # Thsi scenario would most likely be a HTTP GET.
    else:
        context_dict = {}
        context_dict.update(global_context_dict)
        return render_to_response('emgame/login.html', context_dict, context)


# Use the Login_required() decorator to ensure only those Logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is Logged in, we can now just Log them out.
    logout(request)

    context_dict = {}
    context_dict.update(global_context_dict)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/emgame/',context_dict)


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    team_list = Team.objects.order_by('group')

    context_dict = {}
    context_dict['teams']=team_list
    context_dict.update(global_context_dict)

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('emgame/index.html', context_dict, context)


@login_required
def enterpick(request):
    if global_context_dict['tournament_started']:
        raise django.core.exceptions.PermissionDenied
        #return django.http.HttpResponseForbidden()
    logger.info('In enterpicks view, user = {0}'.format(request.user.username))

    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    completed = False
    #A HTTP POST
    if request.method == 'POST':
        pick_form = PickForm(request.POST)

        # Have we been provided witha a valid form?
        if pick_form.is_valid():
            pick = pick_form.save(commit=False)

            #user = models.ForeignKey(UserProfile)
            pick.user = UserProfile.objects.get(user=request.user)

            #pick_date = models.DateTimeField('date entered')
            pick.pick_date =  datetime.datetime.now()


            #pick.pick_name = models.CharField(max_length=80)
            if pick.pick_name == "":
                pick.pick_name =  "{0}'s pick (at {1})".format(pick.user.username,pick.pick_date)

            #scoring = models.ForeignKey(Scoring)
            pick.scoring = Scoring.objects.get(name="ORIGINAL")

            #Leave score and is_truth default
            #score = models.PositiveIntegerField(default=0)
            #is_truth = models.BooleanField(default=False)
            #completed = models.BooleanField(default=False)

            #Have to save before we can add the odd form data
            pick.save()
            for name,value in pick_form.cleaned_data.items():
                if '1st' in name:
                    pick.group_winners.add(Team.objects.get(country=value))
                if '2nd' in name:
                    pick.group_runners_up.add(Team.objects.get(country=value))
                if '3rd' in name:
                    pick.group_third.add(Team.objects.get(country=value))
                if '4th' in name:
                    pick.group_fourth.add(Team.objects.get(country=value))
                if 'sp_qf_' in name:
                    pick.quarterfinal_teams.add(Team.objects.get(country=value))
                if 'sp_sf_' in name:
                    pick.semifinal_teams.add(Team.objects.get(country=value))
                if 'sp_f_' in name:
                    pick.final_teams.add(Team.objects.get(country=value))
                if 'striker' in name:
                    pick.strikers.add(Player.objects.get(name=value))

            err = pick.validate()
            if err is not None:
                logger.info("PICK ERROR: {0}".format(err))
                #Add a custom error to the form
                errors = pick_form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
                errors.append(err)
                pick_form._errors[NON_FIELD_ERRORS] = errors
                #If you want to add an error to a field
                #pick_form._errors[err[0]] = ErrorList([err[1]])

                pick.delete()
                completed = False
            else:
                pick.completed = True
                completed = pick.completed

                # Save the new category to the database.
                pick.save()

                logger.info(pick.print_detail())
                pick.write_file()

                # Now call the index() view.
                # The user will be shown the homepage.
                #return displaypicks(request)
        else:
            # If the request form contained  errors - just print them in the terminal.
            print pick_form.errors
            pick = PickForm()
    else:
        # If the request was not a POST, display the form to enter details.
        pick_form = PickForm()
        pick = PickForm()

    context_dict = {}
    context_dict.update({'form': pick_form, 'completed':completed, 'pick':pick})
    context_dict.update(global_context_dict)
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('emgame/enterpick.html', context_dict, context)



@login_required
def mypicks(request):
    context = RequestContext(request)
    user_name = request.user.username

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {}
    context_dict['user_name']=user_name

    #filter returns all picks or None
    user_picks = Pick.objects.filter(user__user__username=user_name)
    context_dict['user_picks'] = user_picks

    context_dict.update(global_context_dict)

    #A HTTP POST
    #if request.method == 'GET':
    #    pick = Pick(request.GET)
    return render_to_response('emgame/mypicks.html', context_dict, context)


def displaypick(request, pick_id):
    context = RequestContext(request)
    user_name = request.user.username
    context_dict = {}
    try:
        display_pick = Pick.objects.get(id=pick_id)
        if(
            (not global_context_dict['tournament_started']) and
            display_pick.user.user.username != user_name
          ):
           raise django.core.exceptions.PermissionDenied
        context_dict['display_pick'] = display_pick
    except Pick.DoesNotExist:
        raise django.core.exceptions.ObjectDoesNotExist

    group_stage = {1:[],2:[],3:[],4:[]}
    for g1 in display_pick.group_winners.order_by('group__name'):
        g1_dict = {'country': g1.country, 'correct': False}
        if(g1.group_rank == 1):
            g1_dict['correct'] = True
        group_stage[1].append(g1_dict)
    for g2 in display_pick.group_runners_up.order_by('group__name'):
        g2_dict = {'country': g2.country, 'correct': False}
        if(g2.group_rank == 2):
            g2_dict['correct'] = True
        group_stage[2].append(g2_dict)
    for g3 in display_pick.group_third.order_by('group__name'):
        g3_dict = {'country': g3.country, 'correct': False}
        if(g3.group_rank == 3):
            g3_dict['correct'] = True
        group_stage[3].append(g3_dict)
    for g4 in display_pick.group_fourth.order_by('group__name'):
        g4_dict = {'country': g4.country, 'correct': False}
        if(g4.group_rank == 4):
            g4_dict['correct'] = True
        group_stage[4].append(g4_dict)

    quarterfinal_teams = []
    for qft in display_pick.quarterfinal_teams.all():
        qft_dict = {'country': qft.country, 'correct': False}
        if(qft.furthest_round > 2):
            qft_dict['correct'] = True
        quarterfinal_teams.append(qft_dict)

    semifinal_teams = []
    for sft in display_pick.semifinal_teams.all():
        sft_dict = {'country': sft.country, 'correct': False}
        if(sft.furthest_round > 3):
            sft_dict['correct'] = True
        semifinal_teams.append(sft_dict)

    final_teams = []
    for ft in display_pick.final_teams.all():
        ft_dict = {'country': ft.country, 'correct': False}
        if(ft.furthest_round > 4):
            ft_dict['correct'] = True
        final_teams.append(ft_dict)

    champion = {'country': display_pick.champion.country ,
                'correct': display_pick.champion.is_champion }
    #third_place = {'country': display_pick.third_place_team.country ,
    #            'correct': display_pick.third_place_team.is_third_place }

    defensive_team = display_pick.defensive_team

    context_dict['group_stage'] = group_stage
    context_dict['quarterfinal_teams'] = quarterfinal_teams
    context_dict['semifinal_teams'] = semifinal_teams
    context_dict['final_teams'] = final_teams
    context_dict['champion'] = champion
    #context_dict['third_place'] = third_place
    context_dict.update(global_context_dict)
    return render_to_response('emgame/displaypick.html', context_dict, context)


def results(request):
    if not global_context_dict['tournament_started']:
        #return django.http.HttpResponseForbidden()
        raise django.core.exceptions.PermissionDenied
    context = RequestContext(request)

    # Create a context dictionary which we can pass to the template rendering engine.
    #user_list = UserProfile.objects.order_by('score')
    #context_dict = {'users': user_list}
    pick_list = Pick.objects.order_by('-score')
    context_dict = {}
    context_dict['picks'] = pick_list

    last_update_event = Event.objects.get(name='LAST_SCORE_UPDATE')
    context_dict['LAST_SCORE_UPDATE'] = last_update_event.datetime.strftime("%a %b %d %H:%M:%S %Z %Y")

    context_dict.update(global_context_dict)
    return render_to_response('emgame/results.html', context_dict, context)

def scoring(request):
    context = RequestContext(request)

    context_dict = {}
    context_dict.update(global_context_dict)
    
    return render_to_response('emgame/scoring.html', context_dict, context)

