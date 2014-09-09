
from account_manager.models import account_data



def getSessionOrAccountData(request, key):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            record = account_data.objects.get(username=username, key=key)
            return record.value
        except:
            print(key, 'nothing returned')
            return None
    else:
        if key in request.session.keys():
            return request.session[key]
        else:
            return None
    
def setSessionOrAccountData(request, key, value):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            record = account_data.objects.get(username=username, key=key)
            record.value = value
            record.save()
        except account_data.DoesNotExist:
            record = account_data(username=username, key=key, value=str(value))
            record.save()
    else:
        request.session[key] = value
        
def deleteSessionOrAccountData(request, key):
    if request.user.is_authenticated():
        username = request.user.username
        account_data.objects.filter(username=username).filter(key=key).delete()
    else:
        del request.session[key]
        

