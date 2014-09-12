from django.shortcuts import HttpResponse
from django.shortcuts import render, get_object_or_404
from kana.models import base_kana, derived_kana, hiragana_sections, katakana_sections
from account_manager.helpers import getSessionOrAccountData, \
                    setSessionOrAccountData, \
                    deleteSessionOrAccountData
import json
from django.utils.html import strip_tags
                    



def hiragana(request):
    some_kana = base_kana.objects.all().order_by('id')[:15]
    # session management
    next_incomplete_section_found = False
    next_incomplete_section = None
    for i,section in enumerate(hiragana_sections):
        section_finished_key = "hiragana_section_" + str(i) + "_finished"
        section_char_id_key = "hiragana_section_" + str(i) + "_char_id"
        # if section_finished_key in request.session.keys():
        if getSessionOrAccountData(request, section_finished_key):
            hiragana_sections[i]['status'] = "complete"
        # elif section_char_id_key in request.session.keys():
        elif getSessionOrAccountData(request, section_char_id_key):
            hiragana_sections[i]['status'] = getSessionOrAccountData(request, section_char_id_key)
            if not next_incomplete_section_found:
                next_incomplete_section = section['section']
                next_incomplete_section_found = True
        else:
            hiragana_sections[i]['status'] = "not_started"
            if not next_incomplete_section_found:
                next_incomplete_section = section['section']
                next_incomplete_section_found = True
    #end session management
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username
    else:
        logged_in = False
        username = None
    context = {'some_kana': some_kana, 
               'sections': hiragana_sections,
               'next_incomplete_section': next_incomplete_section,
               'logged_in': logged_in,
               'username': username,
               'module_name': "Hiragana",
               'module_number': 1}
    return render(request, 'kana/index.html', context)

def katakana(request):
    some_kana = base_kana.objects.all().order_by('id')[:15]
    # session management
    next_incomplete_section_found = False
    next_incomplete_section = None
    for i,section in enumerate(katakana_sections):
        section_finished_key = "katakana_section_" + str(i) + "_finished"
        section_char_id_key = "katakana_section_" + str(i) + "_char_id"
        # if section_finished_key in request.session.keys():
        if getSessionOrAccountData(request, section_finished_key):
            katakana_sections[i]['status'] = "complete"
        # elif section_char_id_key in request.session.keys():
        elif getSessionOrAccountData(request, section_char_id_key):
            katakana_sections[i]['status'] = getSessionOrAccountData(request, section_char_id_key)
            if not next_incomplete_section_found:
                next_incomplete_section = section['section']
                next_incomplete_section_found = True
        else:
            katakana_sections[i]['status'] = "not_started"
            if not next_incomplete_section_found:
                next_incomplete_section = section['section']
                next_incomplete_section_found = True
    #end session management
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username
    else:
        logged_in = False
        username = None
    context = {'some_kana': some_kana, 
               'sections': katakana_sections,
               'next_incomplete_section': next_incomplete_section,
               'logged_in': logged_in,
               'username': username,
               'module_name': "Katakana",
               'module_number': 2}
    return render(request, 'kana/index.html', context)

def detail(request, kana_id):
    kana = get_object_or_404(base_kana, pk=kana_id)
    # determine if katakana or hiragana
    if kana.id <= hiragana_sections[-1]['end']:
        sections = hiragana_sections
        module_name="hiragana"
    else:
        sections = katakana_sections
        module_name="katakana"
    nextKana = kana.id+1
    previousKana = kana.id-1
    modifications = derived_kana.objects.filter(base_kana_id=kana_id)
    for i,section in enumerate(sections):
        if kana.id >= section['start'] and kana.id <=section['end']:
            section_index = i
            first_in_section = True if kana.id == section['start'] else False
            last_in_section = True if kana.id == section['end'] else False   
            section_name = section['name'] 
            section_name = "Hiragana Section " + str(section['section'])
            break
    section_start_id = sections[section_index]['start'] - 1
    section_end_id = sections[section_index]['end'] - 1
    section_kanas = base_kana.objects.all().order_by('id')[section_start_id:section_end_id+1]
    if kana.id == sections[-1]['end']:
        last_in_module = True
    else:
        last_in_module = False
    if kana.id == sections[0]['start']:
        first_in_module = True
    else:
        first_in_module = False
    # session management
    section_finished_key = module_name + "_section_" + str(section_index) + "_finished"
    section_char_id_key = module_name + "_section_" + str(section_index) + "_char_id"
    if not section_finished_key in request.session.keys():
        if last_in_section:
            setSessionOrAccountData(request, section_finished_key, True)
            deleteSessionOrAccountData(request, section_char_id_key)
            module_finished = True
            for i,section in enumerate(sections):
                this_section_finished_key = module_name + "_section_" + str(i) + "_finished"
                # if not this_section_finished_key in request.session.keys():
                if not getSessionOrAccountData(request, this_section_finished_key):
                    module_finished = False
            if module_finished:
                setSessionOrAccountData(request, module_name + '_module_finished', True)
        elif not first_in_section:            
            setSessionOrAccountData(request, section_char_id_key, kana_id)
            setSessionOrAccountData(request, module_name + '_module_started', True)
    user_mnemonic = getSessionOrAccountData(request, 'kana_mnemonic_' + kana_id)
    # end session management
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username
    else:
        logged_in = False
        username = None
    context = {'kana': kana, 
               'nextKana': nextKana, 
               'previousKana': previousKana,
               'section_kanas': section_kanas, 
               'modifications': modifications,
               'section_index': section_index,
               'section': sections[section_index],
               'section_name': section_name,
               'module_name': module_name,
               'first_in_section': first_in_section,
               'last_in_section': last_in_section,
               'logged_in': logged_in,
               'username': username,
               'user_mnemonic': user_mnemonic,
               'last_in_module': last_in_module,
               'first_in_module': first_in_module,}
    return render(request, 'kana/detail.html', context)

def results(request, kana_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % kana_id)

def mnemonics_handler(request):
    if request.is_ajax():
        key = "kana_mnemonic_" + request.GET['kana_number']
        setSessionOrAccountData(request, 
                                key,
                                strip_tags(request.GET['mnemonics_text']))
        result = getSessionOrAccountData(request, key)
        if not result:
            kana = get_object_or_404(base_kana, pk=request.GET['kana_number'])
            result = kana.mnemonic
        return HttpResponse(json.dumps( {'mnemonics_text': result} ))

def test(request):
    return render(request, 'kana/test.html', None)


            
        


