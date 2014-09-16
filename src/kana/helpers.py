# coding=utf-8

from kana.models import kana, combinations
from django.core.urlresolvers import reverse
from account_manager.helpers import getSessionOrAccountData



def add_popovers(request, string):
    popover_string = ''
    for char in string:
        # if not found in database, simply return character
        try:
            kana_record = kana.objects.get(kana=char)
        except:
            popover_string += char
            continue            
        # if appropriate, get parent kana for link
        if kana_record.kana_order == 0:
            parent_record = kana.objects.get(kana=kana_record.parent)
            kana_link = parent_record.kana_order
            personal_mnemonic_key = "kana_mnemonic_" + str(parent_record.kana_order)
        else:
            kana_link = kana_record.kana_order
            personal_mnemonic_key = "kana_mnemonic_" + str(kana_record.kana_order)
        mnemonic =  getSessionOrAccountData(request, personal_mnemonic_key)
        if mnemonic:
            mnemonic = "<em>mnemonic:</em> " + mnemonic + "<br><br>"
        else:
            mnemonic = ''
        popover_string += '''<a href="#" class="add_popover" style="text-decoration: none;" 
        rel="popover" data-placement="bottom"
        data-content="''' + \
                mnemonic + \
        '''<a href=\'''' + reverse('kana:detail', kwargs={'kana_order': kana_link}) + '''\'>More...</a>"
        data-original-title="<span style='color:#CC5200;font-size:25px'>''' \
        + kana_record.kana +'</span> &nbsp;&nbsp;[ ' + kana_record.pronunciation + ' ]">' + kana_record.kana + '</a>'        
    return popover_string

def get_kana_link(char):
    kana_record = kana.objects.get(kana=char)
    if kana_record.kana_order == 0:
        parent_record = kana.objects.get(kana=kana_record.parent)
        kana_link = parent_record.kana_order
    else:
        kana_link = kana_record.kana_order
    return kana_link

def tab(string, indent=0):
    indent_string = ''
    for i in range(0,indent):
        indent_string += '    '
    return '\n' + indent_string + string

def get_pronunciation(char):
    # skip if not in database
    try:
        for mychar in char:
            kana_record = kana.objects.get(kana=mychar)
    except:
        print("exception")
        return ""
    if len(char) == 1:
        kana_record = kana.objects.get(kana=char)
        return kana_record.pronunciation
    elif 'っ' in char:
        kana_record = kana.objects.get(kana=char[1])
        return kana_record.pronunciation[0] + kana_record.pronunciation
    elif 'ー' in char:
        kana_record = kana.objects.get(kana=char[0])
        return kana_record.pronunciation + kana_record.pronunciation[-1]
    else:
        try:
            kana_record = combinations.objects.get(kana=char)
        except:
            return ""
        return kana_record.pronunciation

def string_to_char_list(string): 
    group_with_before = ('ゃ', 'ゅ', 'ょ', 'ャ', 'ュ', 'ョ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ー')
    group_with_after = ('っ',)
    char_list = []
    for char in string:
        if char in group_with_after:
            char_temp = char
        elif char in group_with_before:
            char_list[-1] += char
        else:
            if 'char_temp' in locals():
                char_list.append(char_temp + char);
                del char_temp
            else:
                char_list.append(char)
    return char_list  

def practicify(request, string):
    # create groups for get_pronunciation
    char_list = string_to_char_list(string)
    # end create groups
    mystr = tab('<table class="center_table">')
    mystr += tab("<tr>",1)
    for char in char_list:
        mystr += tab('<td class="pronunciation">' + get_pronunciation(char) + '</td>', 2)
    mystr += tab('</tr>',1)
    mystr += tab("<tr>",1)
    for char in char_list:
        mystr += tab('<td class="char">' + add_popovers(request, char) + '</td>', 2)
    mystr += tab("</tr>",1)
    mystr += tab("</table>")
    return mystr


