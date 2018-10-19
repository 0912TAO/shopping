from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect           # 重定向
from django.core.urlresolvers import reverse    # 反解析

from django.contrib.auth.models import User

from io import BytesIO

from . import utils

# 主页
def index(request):
    return render(request, "mall/index.html", {})


# 注册
def register(request):
    if request.method == "GET":
        return render(request, 'mall/register.html', {})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        querenpassword = request.POST['querenpassword']
        user = User.objects.create_user(username=username,password=password)
        user.save()
        return render(request, "mall/login.html", {"msg":"恭喜注册成功，请登录"})




# 验证码
def code(request):
    img, code = utils.create_code()
    # 首先需要将code 保存到session 中
    request.session['code'] = code
    # 返会图片
    file = BytesIO()
    img.save(file, 'PNG')

    return HttpResponse(file.getvalue(), "image/png")


# 登录
def user_login(request):
    # GET方式打开页面
    if request.method == 'GET':
        return render(request, 'mall/user_login.html', {})

    # POST方式打开页面
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

    try:
        user = User.objects.get(username=username, password=password)
        print(user)
    except:
        return render(request, 'mall/login.html', {"msg":"账号或密码错误，请重新输入"})


# 商品信息
def commodity_info(request):
    pass


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

