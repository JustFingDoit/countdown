# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.context_processors import csrf

#from triggers.models import Trigger, TriggerManager, Message

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
    user.triggers.create(description='testtrigger', frequency=30, interval='days', next_checkin=next_checkin)
    return HttpResponse("User created")

def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                 password=request.POST['password'])
        if user is not None:
            request.session['logged_in'] = user.id
            trigger = user.triggers.get(owner=user)
            trigger.checkin()
            trigger.save()
            c = {'next': trigger.next_checkin}
            c.update(csrf(request))
            return render_to_response('message.html', c)
            #return HttpResponse("Checked in! Next check in date must be before " + 
            #       str(trigger.next_checkin))
    return HttpResponse("Failure!")
    
def set_message(request):
    user = User.objects.get(id=request.session['logged_in'])
    if request.method == 'POST' and user is not None:
        user.message.create(to=request.POST['to_address'], 
                subject=request.POST['subject'], message=request.POST['message'])
        c = {'message': request.POST}
        c.update(csrf(request))
        return render_to_response('message.html', c)
    return HttpResponse("Error!")
    
