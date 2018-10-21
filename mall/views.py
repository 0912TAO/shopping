from django.shortcuts import render
from django.shortcuts import redirect
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
                request.session["loginUser"] = user
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
        # return render(request, 'mall/user_login.html', {})
        try:
            next_url = request.GET['next']
        except:
            next_url = "/mall/"

        if next_url == "/mall/user_logout/":
            next_url = "/mall/"

        return render(request, 'mall/user_login.html', {"next_url": next_url})
    # POST方式打开页面
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get("next", "/mall/")

        if next_url == "/mall/user_logout/":
            next_url = "/mall/"

        user = authenticate(username=username, password=password)
        request.session["loginUser"] = user
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_url)
                # return render(request, 'mall/index.html', {"user": user})
            else:
                return render(request, 'mall/user_login.html', {"msg": "您的账号已被禁用，请联系管理员"})
        else:
            return render(request, 'mall/user_login.html', {"msg": "账号或密码错误，请重新登录"})


# 退出登录
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'mall/user_login.html', {"msg":"您已成功退出！"})


# 个人中心
@login_required
def personal(request):
    userA = models.UserA.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        return render(request, "mall/personal.html", {"userA": userA})
    if request.method == 'POST':
        pass


# 修改个人资料
def changeinfo(request):
    userA = models.UserA.objects.get(user_id = request.user.id)
    if request.method == "GET":
        return render(request, "mall/changeinfo.html", {"userA": userA})
    else:
        gender = request.POST.get('gender', 0)
        age = request.POST.get('age', 1)
        phone = request.POST.get('phone', "")
        add = request.POST.get('add', "")
        print(gender,age,phone,add)

        userA.gender = gender
        userA.age = age
        userA.phone = phone
        userA.add = add
        userA.save()
        return render(request, "mall/changeinfo.html", {"userA": userA,"msg": "修改个人信息成功"})



# 更改头像
@login_required
def changeheader(request):
    userA = models.UserA.objects.get(user=request.user.id)
    if request.method == "GET":
        print(request.user.id)
        print("********")
        print(userA)
        print("-----------")
        return render(request, "mall/changeheader.html", {"userA": userA})
    elif request.method == "POST":
        header = request.FILES.get("header", "static/image/default.jpg")
        print(header)
        print("获取到头像数据")
        userA.header = header
        userA.save()
        return render(request, "mall/changeinfo.html", {"msg": "头像修改成功", "userA":userA})
        # return reverse("mall/changeinfo.html", )

# 验证旧密码
def check_password(request, old_password):
    u = User.objects.get(pk=request.user.id)
    print(u)
    print(u.username)
    user = authenticate(username=u.username, password=old_password)
    if user is None:
        return JsonResponse({"msg": "输入的旧密码不正确", "success": False})
    else:
        return JsonResponse({"msg": "正确", "success": True})


# 更改密码
@login_required
def changepwd(request):
    u = User.objects.get(pk=request.user.id)
    userA = models.UserA.objects.get(user_id = request.user.id)
    print(userA)
    if request.method == "GET":
        return render(request, "mall/changepwd.html", {"userA": userA})
    if request.method == "POST":
        old_password = request.POST['old_password']
        password = request.POST['password']
        two_password = request.POST['two_password']

        print(old_password, password, two_password)

        user = authenticate(username=u.username, password=old_password)

        if user is None:
            return JsonResponse({"msg": "输入的旧密码不正确", "success": False})
        if len(password) < 6:
            return JsonResponse({"msg": "输入的新密码小于6位", "success": False})
        if password != two_password:
            return JsonResponse({"msg": "两次输入密码不一致", "success": False})

        try:
            # user = User.objects.create_user(username=u.username, password=password)
            # user.save()
            u.set_password(password)
            u.save()
            return JsonResponse({"msg": "修改密码成功", "success": True})
        except:
            return JsonResponse({"msg": "修改密码失败", "success": False})


# 商品购买
def product(request):
    return render(request, "mall/product.html", {})


# 商品详情
def xiangqing(request):
    return render(request, "mall/xiangqing.html", {})


# 商品评论
def pinglun(request):
    return render(request, "mall/pinglun.html", {})


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


# 订单中心
def orders(request):
    return render(request, 'mall/orders.html', {})





# 服务管理
def services(request):
    return render(request, 'mall/services.html', {})




