from django.shortcuts import HttpResponse
from django.shortcuts import render, get_object_or_404
from kana.models import kana, hiragana_sections
from account_manager.models import account_data

from master_the_jouyou.forms import UserForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User


from django.utils import timezone
from account_manager.helpers import getSessionOrAccountData, \
                    setSessionOrAccountData, \
                    deleteSessionOrAccountData



def index(request):
    # session management
    # if 'hiragana_module_started' in request.session.keys():
    if getSessionOrAccountData(request, 'hiragana_module_started'):
        hiragana_module_started = True
    else:
        hiragana_module_started = False
    # if 'hiragana_module_finished' in request.session.keys():
    if getSessionOrAccountData(request, 'hiragana_module_finished'):
        hiragana_module_finished = True
    else:
        hiragana_module_finished = False
    # if 'katakana_module_started' in request.session.keys():
    if getSessionOrAccountData(request, 'katakana_module_started'):
        katakana_module_started = True
    else:
        katakana_module_started = False
    # if 'katakana_module_finished' in request.session.keys():
    if getSessionOrAccountData(request, 'katakana_module_finished'):
        katakana_module_finished = True
    else:
        katakana_module_finished = False
    #end session management
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username
    else:
        logged_in = False
        username = None
    context = {'hiragana_module_started': hiragana_module_started, 
               'hiragana_module_finished': hiragana_module_finished,
               'katakana_module_started': katakana_module_started, 
               'katakana_module_finished': katakana_module_finished,
               'logged_in': logged_in,
               'username': username,
               # 'next_incomplete_section': next_incomplete_section
               }
    return render(request, 'home.html', context)

def adduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # django is forcing me to define last_login for create_user method
            # I can't figure out for the life of me why
            form.cleaned_data['last_login'] = timezone.now()
            print(form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
            # save all existing session data to new user account
            for key in request.session.keys():
                record = account_data(username=request.POST['username'], 
                                      key=key, 
                                      value=str(request.session[key]))
                record.save()
            #login new user
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return redirect('adduser_confirmation')
    else:
        form = UserForm() 
    return render(request, 'adduser.html', {'form': form}) 

def adduser_confirmation(request):
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username
        email = User.objects.get(username=request.user.username).email
    else:
        return redirect('adduser')
    context = {
               'logged_in': logged_in,
               'username': username,
               'email': email,
               }
    return render(request, 'adduser_confirmation.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

