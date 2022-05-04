import hashlib

from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import User

# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        return render(request,'register/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_agin = request.POST['password_agin']
        if (password != password_agin):
            return HttpResponse('两次密码输入不一致')
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        #下面这条语句返回的是批量数据
        old_users = User.objects.filter(username = username)
        if old_users:
            return HttpResponse('用户名已注册')
        try:
            #下面这一块儿有可能报错重复插入，加上try捕获异常
            user = User.objects.create(username=username,password=password_m)
        except Exception as e:
            print('create user error s %s'%(e))
            return HttpResponse('用户名已注册')
        #在下面使用保存session的方式，获取登录状态，保存session至服务器
        request.session['username'] = username
        request.session['user_id'] = user.id
        return HttpResponseRedirect('/notes')
def login_view(request):
    if request.method == 'GET':
        #检查登录状态，如果是已经登录过了，显示已登录信息，先检查保存至数据库里面的session，如果没有信息继续查找保存至浏览器的cookies信息，如果还是没有则立即返回登录界面
        """检查session"""
        if request.session.get('username') and request.session.get('user_id'):
            return HttpResponseRedirect('/notes')
        """检查cookies"""
        c_username = request.COOKIES.get('username')
        c_user_id = request.COOKIES.get('user_id')
        if c_user_id and c_username:
            request.session['username'] = c_username#回写session
            request.session['user_id'] = c_user_id
            return HttpResponseRedirect('/notes')
        """如果session和cookies都没有找到则返回登录界面供用户登录"""
        return render(request,'register/login.html')
    elif request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)#这里捕获异常只能是没有查到用户名，因为数据库中设置了这个字段是唯一的，不可能是查多了
        except Exception as e:
            print('login user error is %s'%(e))
            return HttpResponse('用户名或者密码错误')
        m = hashlib.md5()
        m.update(password.encode())
        #密码校验
        if m.hexdigest() != user.password:
            return HttpResponse('用户名或者密码错误')
        #保存session
        request.session['username'] = username
        request.session['user_id'] = user.id
        return HttpResponseRedirect('/notes')
        #判断是否记住用户名,request.POST返回的是字典，所以直接判断某个字符串是否是字典的键即可
        if 'remember' in request.POST:
            resp.set_cookie('username',username,3600*24*3)#保存cookie至客户端浏览器
            resp.set_cookie('user_id',user.id,3600*24*3)




        return resp
def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'user_id' in request.session:
        del request.session['user_id']
    resp = HttpResponseRedirect('/notes')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'user_id' in request.COOKIES:
        resp.delete_cookie('user_id')
    return resp






