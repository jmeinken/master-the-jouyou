from django.shortcuts import HttpResponse
from django.shortcuts import render, get_object_or_404
from kana.models import base_kana, derived_kana, hiragana_sections
from account_manager.models import account_data

from ReadJapanese.forms import UserForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User


from django.utils import timezone
from account_manager.helpers import getSessionOrAccountData, \
                    setSessionOrAccountData, \
                    deleteSessionOrAccountData



def index(request):
    # session management
    # if 'hiragana_section_started' in request.session.keys():
    if getSessionOrAccountData(request, 'hiragana_section_started'):
        hiragana_section_started = True
    else:
        hiragana_section_started = False
    # if 'hiragana_section_finished' in request.session.keys():
    if getSessionOrAccountData(request, 'hiragana_section_finished'):
        hiragana_section_finished = True
    else:
        hiragana_section_finished = False
    #end session management
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username
    else:
        logged_in = False
        username = None
    context = {'hiragana_section_started': hiragana_section_started, 
               'hiragana_section_finished': hiragana_section_finished,
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
            return redirect('home')
    else:
        form = UserForm() 

    return render(request, 'adduser.html', {'form': form}) 

def logout_user(request):
    logout(request)
    return redirect('home')

