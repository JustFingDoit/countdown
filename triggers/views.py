# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from triggers.models import Trigger, TriggerManager

def home(request):
    #Render a page where user can signup or login
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)
    
def create_user(request):
    if request.method == 'GET':
        return home()
    user = User()
    user.username = request.POST['username']
    user.email = request.POST['email']
    #doesn't confirm pw
    user.set_password(request.POST['password'])
    #Doesn't validate form
    user.save()
    import datetime
    #create trigger
    next_checkin = datetime.datetime.now() + datetime.timedelta(days=30)
    user.triggers.create(description='testtrigger', frequency=60, interval='minutes', next_checkin=next_checkin)
    return HttpResponse("User created")

def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                 password=request.POST['password'])
        if user is not None:
            #trigger = user.triggers.get(owner_id=user.id)
            trigger = user.triggers.get(id=1)
            if len(trigger) > 0:
                trigger[0].checkin()
            else:
                return HttpResponse("Failure! ddddd")            
            return HttpResponse("Checked in!")
    return HttpResponse("Failure!")            
