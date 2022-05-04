from django.http import HttpResponseRedirect
def redirect_log(request):
    return HttpResponseRedirect('/register_login/login/')