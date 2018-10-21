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
<<<<<<< HEAD
        return render(request, 'mall/user_login.html', {})
=======
        try:
            next_url = request.GET['next']
        except:
            next_url = "/mall/"
        return render(request, 'mall/user_login.html', {"next_url": next_url})

>>>>>>> 721bbb2cf3c7641f3d3ee2e955f082da4de6d0c0
    # POST方式打开页面
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        next_url = request.POST.get("next", "/mall/")
        print(next_url)
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


# 完善个人资料
@login_required
def overself(request):
    if request.method == 'GET':
        return render(request, "overself.html", {})
    if request.method == 'POST':
        pass

# 更改头像
@login_required
def change_header(request):
    user = models.UserA.objects.get(user=request.user.id)
    if request.method == "GET":
        print(request.user.id)
        print("********")
        print(user)
        print("-----------")
        return render(request, "change_header.html", {"user": user})
    elif request.method == "POST":
        header = request.FILES.get("header","static/images/1(1).jpeg")
        print(header)
        print("获取到头像数据")
        user.herder = header
        user.save()
        return render(request, "change_header.html", {"msg": "头像修改成功"})


# 更改密码
@login_required
def change_password(request):
    user = User.objects.get(pk = request.user.id)
    print(user)
    if request.method == "GET":
        return render(request, "change_header.html", {})
    if request.method == "POST":
        old_password = request.POST['old_password']
        password = request.POST['password']
        two_password = request.POST['two_password']

        user = authenticate(password=old_password)
        if user is None:
            return render(request, "change_password.html", {"msg": "旧密码不正确"})
        if len(password) < 6:
            return render(request, "change_password.html", {"msg": "新密码不能小于6位"})
        if password != two_password:
            return render(request, "change_password.html", {"msg": "两次输入密码不一致"})
        try:
            user = User.objects.create_user(password=password)
            user.save()
            return render(request, "user_login.html", {"msg": "修改密码成功"})
        except:
            return render(request, "change_password.html", {"msg": "修改密码失败"})


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


<<<<<<< HEAD
# 开店申请页面 没有登录不能进入
def open_shop(request):
    # 邮箱必须已经绑定弹窗提示

    return render(request, "mall/open_shop.html", {})
=======
# 订单中心
def orders(request):
    return render(request, 'mall/orders.html', {})


# 个人中心
def Personal(request):
    try:
        user = request.session["loginUser"]
        print(1231231231)
        print(1231231231)
        return render(request, "blog/show.html", {"user": user})

    except:
        return render(request, "blog/failed.html", {"msg1": "未登录，请先登录！！"})

    return render(request, 'mall/Personal.html', {})


# 服务管理
def services(request):
    return render(request, 'mall/services.html', {})


# 修改信息
def changeinfo(request,u_id):
    if request.method == "GET":
        user = models.User.objects.filter(id=u_id).first()
        return render(request, "blog/changeinfo.html", {"user": user})
    else:
        gender = request.POST['gender']
        age = request.POST['age']
        phone = request.POST['phone']
        add = request.POST['add']
        user = models.User.objects.get(pk=u_id)
        user.gender = gender
        user.age = age
        user.save()
        user.phone = phone
        user.add = add
        user.save()
        return redirect("/blog/changeinfo/" + str(u_id) + "/")

# 修改密码
def changepwd(request):

    users = request.session["loginUser"]
    # users = models.User.objects.filter(id=u.id)
    loginpassword = request.POST["userpassword"].strip()
    print("初始密码" + loginpassword)
    newloginpassword = request.POST["newnpassword"].strip()
    print("新密码" + newloginpassword)
    qnewloginpassword = request.POST["qnewnpassword"].strip()
    print("输入新密码" + newloginpassword)
    loginpassword = utils.hmac_by_md5(loginpassword)
    if loginpassword != users.password:
        return render(request, "blog/changepwd.html", {"msg1": "旧密码错误请重新输入！！"})
    if newloginpassword != qnewloginpassword:
        return render(request, "blog/changepwd.html", {"msg1": "两次密码不一样！！"})
    else:
        newloginpassword = utils.hmac_by_md5(newloginpassword)
        users.password = newloginpassword
        users.save()
        return redirect(reverse("blog:logout"))
>>>>>>> b467693ba9af16585f28e4e612ceb5cd2c8a6593
