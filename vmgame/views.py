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

#vmgame
from vmgame.models import Team, Player, Group, User, Scoring, UserProfile,GROUP_LETTERS,GROUP_RANKS
from vmgame.forms import PickForm, UserForm, UserProfileForm

logger = logging.getLogger(__name__)

def register(request):
    logger.info('In request view')
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
        
    # Render the template depending on the context.
    return render_to_response(
        'vmgame/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        #{'user_form': user_form, 'registered': registered},
        context)

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
                return HttpResponseRedirect('/vmgame/')
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
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('vmgame/login.html', {}, context)  
        
# Use the Login_required() decorator to ensure only those Logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is Logged in, we can now just Log them out.
    logout(request)
    
    # Take the user back to the homepage.
    return HttpResponseRedirect('/vmgame/')      

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    team_list = Team.objects.order_by('group')
    context_dict={'teams':team_list}
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('vmgame/index.html', context_dict, context)    


@login_required  
def enterpicks(request):
    logger.info('In enterpicks view, user = {0}'.format(request.user.username))
    
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    
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


            #pick_name = models.CharField(max_length=80)
            if pick.pick_name == "":
                pick.pick_name =  "{0}'s pick (at {1})".format(pick.user.username,pick.pick_date)

            #scoring = models.ForeignKey(Scoring)
            pick.scoring = Scoring.objects.get(name="ORIGINAL")

            #Leave score and is_truth default
            #score = models.PositiveIntegerField(default=0)
            #is_truth = models.BooleanField(default=False)
            #completed = models.BooleanField(default=False)

            pick.completed = True

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


            #TODO: validate

            #TODO if not valid pick.delete
            # Save the new category to the database.
            pick.save()

            logger.info(pick.print_detail())
            # Now call the index() view.
            # The user will be shown the homepage.
            #TODO: Should notify user that pick was successfully entered
            return index(request)
        else:
            # If the request form contained  errors - just print them in the terminal.
            print pick_form.errors

    else:
        # If the request was not a POST, display the form to enter details.
        pick_form = PickForm()
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('vmgame/enterpicks.html', {'form': pick_form}, context)


#Not necessary
#@login_required    
#def restricted(request):
#    return HttpResponse("Since you're logged in, you can see this text!")    

