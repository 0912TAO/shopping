from django.shortcuts import render
from django.shortcuts import redirect           # 重定向
from django.core.urlresolvers import reverse    # 反解析


# 主页
def index(request):
    pass


# 注册
def register(request):
    pass


# 登录
def login(request):
    # GET方式打开页面
    if request.method == 'GET':
        return render(request, 'mall/login.html', {})

    # POST方式打开页面
    elif request.method == 'POST':
        pass


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

