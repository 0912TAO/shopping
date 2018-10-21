from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required   # 需要登陆的装饰器

from django.shortcuts import redirect           # 重定向
from django.core.urlresolvers import reverse    # 反解析

from django.contrib.auth.models import User

from io import BytesIO

from . import utils
from . import models


# 主页
def index(request):
    return render(request, "mall/index.html", {})


# 注册
@transaction.atomic
def register(request):
    if request.method == "GET":
        return render(request, 'mall/register.html', {})
    elif request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        querenpassword = request.POST['querenpassword'].strip()
        code = request.POST['code']
        print(username, password, code)
        if code.upper() != request.session['code'].upper():
            return render(request, 'mall/register.html', {"msg": "验证码不正确，请重新注册"})
        if len(password) < 6:
            return render(request, 'mall/register.html', {"msg": "密码长度不足6位，请重新注册"})
        if password != querenpassword:
            return render(request, 'mall/register.html', {"msg": "两次输入密码不一致，请重新注册"})

        try:
            hyd = transaction.savepoint()
            User.objects.get(username=username)
            return render(request, 'mall/register.html', {"msg":"用户名已存在，请重新注册"})
        except:
            try:
                user = User.objects.create_user(username=username, password=password)
                usera = models.UserA(user=user)
                user.save()
                usera.save()
                transaction.savepoint_commit(hyd)

                return render(request, "mall/user_login.html", {"msg": "恭喜注册成功，请登录"})
            except:
                transaction.savepoint_rollback(hyd)
                return render(request, "mall/register.html", {"msg": "注册失败，请重新注册"})


# 验证码
def code(request):
    img, code = utils.create_code()
    # 首先需要将code 保存到session 中
    request.session['code'] = code
    # 返会图片
    file = BytesIO()
    img.save(file, 'PNG')

    return HttpResponse(file.getvalue(), "image/png")


# ajax检测验证码
def checkcode(request, yzm):
    my_code = request.session['code']
    print(my_code)
    if yzm.upper() != my_code.upper():
        return JsonResponse({"msg":"验证码错误，请重新输入","success":False})
    else:
        return JsonResponse({"msg":"验证码正确", "success":True})


# ajax检测是否用户名是否存在
def checkusername(request, uname):
    try:
        User.objects.get(username=uname)
        return JsonResponse({"msg": "用户名已存在，请重新输入", "success": False})
    except:
        return JsonResponse({"msg": "请继续输入", "success": True})


# 登录
def user_login(request):
    # GET方式打开页面
    if request.method == 'GET':
        return render(request, 'mall/user_login.html', {})

    # POST方式打开页面
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'mall/index.html', {"user": user})
            else:
                return render(request, 'mall/user_login.html', {"msg": "您的账号已被禁用，请联系管理员"})
        else:
            return render(request, 'mall/user_login.html', {"msg": "账号或密码错误，请重新登录"})


# 退出登录
def user_logout(request):
    logout(request)
    return render(request, 'mall/user_login.html', {})


# 商品详情
def product(request):
    return render(request, "mall/product.html", {})


# 购物车添加成功页面
def add_cart(request):
    pass


# 购物车
def my_cart(request):
    # GET方式打开页面
    if request.method == 'GET':
        return render(request, 'mall/my_cart.html', {})

    # POST方式打开页面
    elif request.method == 'POST':
        pass


# 开店申请页面 没有登录不能进入
def open_shop(request):
    # 邮箱必须已经绑定弹窗提示

    return render(request, "mall/open_shop.html", {})