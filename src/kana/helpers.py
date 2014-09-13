from kana.models import base_kana
from django.core.urlresolvers import reverse
from account_manager.helpers import getSessionOrAccountData



def add_popovers(request, string):
    popover_string = ''
    for char in string:
        kana = base_kana.objects.get(kana=char)
        personal_mnemonic_key = "kana_mnemonic_" + str(kana.id)
        mnemonic =  getSessionOrAccountData(request, personal_mnemonic_key)
        if mnemonic:
            mnemonic = "<em>mnemonic:</em> " + mnemonic + "<br><br>"
        else:
            mnemonic = ''
        popover_string += '''
        <a href="#" class="add_popover" style="text-decoration: none;" 
        rel="popover" 
        data-content="''' + \
                mnemonic + '''
                <a href=\'''' + reverse('kana:detail', kwargs={'kana_id': kana.id}) + '''\'>More...</a>"
        data-original-title="<span style='color:#CC5200;font-size:25px'>''' \
        + kana.kana +'</span> &nbsp;&nbsp;[ ' + kana.pronunciation + ' ]">' + kana.kana + '</a>'        
    return popover_string