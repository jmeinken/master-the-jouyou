
from account_manager.models import account_data



def getSessionOrAccountData(request, key):
    if request.user.is_authenticated():
        username = request.user.username
        record = account_data.objects.filter(username=username).filter(key=key)
        return record[0]['value']
    else:
        return request.session[key]
    
def setSessionOrAccountData(request, key, value):
    if request.user.is_authenticated():
        username = request.user.username
        record = account_data(username=username, key=key, value=str(value))
        record.save()
    else:
        request.session[key] = value
