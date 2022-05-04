from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import re
class mymiddlware(MiddlewareMixin):
    def process_request(self,request):
        print('MYMW process_request do')
class mymiddlware2(MiddlewareMixin):
    def process_request(self,request):
        print('MYMW process_request do111111111111')
class visitlimit(MiddlewareMixin):
    visit_time = {}
    a = 0
    def process_request(self,request):
        ip_address = request.META['REMOTE_ADDR']
        path_url = request.path_info
        if not re.match('^/notes',path_url):
            return
        times = self.visit_time.get(ip_address,0)
        print('ip',ip_address,'已经访问',times)
        self.visit_time[ip_address] = times + 1
        if times<5:
            return
        return HttpResponse('您已经访问过'+str(times)+'次，访问被禁止')

