from kana.models import kana
from django.core.urlresolvers import reverse
from account_manager.helpers import getSessionOrAccountData



def add_popovers(request, string):
    popover_string = ''
    for char in string:
        kana_record = kana.objects.get(kana=char)
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
        popover_string += '''
        <a href="#" class="add_popover" style="text-decoration: none;" 
        rel="popover" data-placement="bottom"
        data-content="''' + \
                mnemonic + '''
                <a href=\'''' + reverse('kana:detail', kwargs={'kana_order': kana_link}) + '''\'>More...</a>"
        data-original-title="<span style='color:#CC5200;font-size:25px'>''' \
        + kana_record.kana +'</span> &nbsp;&nbsp;[ ' + kana_record.pronunciation + ' ]">' + kana_record.kana + '</a>'        
    return popover_string

def tab(string, indent=0):
    indent_string = ''
    for i in range(0,indent):
        indent_string += '    '
    return '\n' + indent_string + string

def get_pronunciation(char):
    kana_record = kana.objects.get(kana=char)
    return kana_record.pronunciation
    

def practicify(request, string):
    # create groups for get_pronunciation
       
    # end create groups
    mystr = tab('<table class="center_table">')
    mystr += tab("<tr>",1)
    for char in string:
        mystr += tab('<td class="pronunciation">' + get_pronunciation(char) + '</td>', 2)
    mystr += tab('</tr>',1)
    mystr += tab("<tr>",1)
    for char in string:
        mystr += tab('<td class="char">' + add_popovers(request, char) + '</td>', 2)
    mystr += tab("</tr>",1)
    mystr += tab("</table>")
    return mystr

