from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import Notes
# Create your views here.
def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'username' not in request.session or 'user_id' not in request.session:
            c_username = request.COOKIES.get('username')
            c_user_id =request.COOKIES.get('user_id')
            if not c_username or not c_user_id:
                return HttpResponseRedirect('/register_login/login')
            else:
                request.session['username'] = c_username
                request.session['user_id'] = c_user_id

        return fn(request,*args,**kwargs)
    return wrap
#使用装饰器校验登录状态
@check_login
def add_notes(request):
    notes = Notes.objects.filter(user_id=request.session['user_id'])
    # user =
    if request.method =='GET':
        pag_num = request.GET.get('page',1)#获得请求的页码，首次请求时没有页码传入视图函数，所以使用get函数在第二个参数位置设置没有page值时默认是1
        paginator = Paginator(notes,3)#把所有数据notes按照每页3条数据进行分页
        c_page = paginator.page(int(pag_num))#获取当前页面,在html中可以直接使用for p in c_page,p.title的方式取得对象的某个字段值
        return render(request,'display_notes/pages.html',locals())#把数据传入html文件
        # return render(request,'display_notes/add_notes.html',locals())
    elif request.method =='POST':
        #处理数据
        user_id = request.session['user_id']
        title = request.POST['title']
        content = request.POST['content']
        Notes.objects.create(title=title,content=content,user_id=user_id)

        return HttpResponse('添加笔记成功')
def del_notes(request,id):
    note = Notes.objects.get(id = id)
    note.delete()
    return HttpResponseRedirect('/display_notes/add_notes')
def del_all_notes(request,user_id):
    user_id = user_id
    notes = Notes.objects.filter(user_id=user_id)
    notes.delete()
    return HttpResponseRedirect('/display_notes/add_notes')


