from django.shortcuts import HttpResponse
from django.shortcuts import render, get_object_or_404
from kana.models import base_kana, derived_kana, hiragana_sections



def index(request):
    # session management
    if 'hiragana_section_started' in request.session.keys():
        hiragana_section_started = True
    else:
        hiragana_section_started = False
    if 'hiragana_section_finished' in request.session.keys():
        hiragana_section_finished = True
    else:
        hiragana_section_finished = False
    #end session management
    context = {'hiragana_section_started': hiragana_section_started, 
               'hiragana_section_finished': hiragana_section_finished,
               # 'next_incomplete_section': next_incomplete_section
               }
    return render(request, 'home.html', context)

