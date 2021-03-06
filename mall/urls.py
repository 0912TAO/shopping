from django.conf.urls import  url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),                                          # 主页
    url(r'^index/$', views.index, name='index'),                                    # 主页
    url(r'^code/$', views.code, name='code'),
    url(r'^register/$', views.register, name='register'),                           # 注册
    url(r'^user_login/$', views.user_login, name='user_login'),                     # 登录
    # 验证验证码
    url(r'^(\w+)/checkcode/$', views.checkcode, name='checkcode'),
    # 验证用户名是否存在
    url(r'^(\w+)/checkusername/$', views.checkusername, name='checkusername'),
    # 退出登录
    url(r'^user_logout/$', views.user_logout, name="user_logout"),
    # 修改个人信息
    url(r'^changeinfo/$', views.changeinfo, name="changeinfo"),
    # 修改用户头像
    url(r'^changeheader/$', views.changeheader, name="changeheader"),
    # 修改用户密码
    url(r'^changepwd/$', views.changepwd, name="changepwd"),
    # 验证密码是否正确
    url(r'^(\w+)/check_password/$', views.check_password, name='check_password'),
    # 个人中心
    url(r'^personal/$', views.personal, name="personal"),
    # 服务？？？
    url(r'^services/$', views.services, name="services"),
    # 商品购买
    url(r'^product/$', views.product, name="product"),
    # 商品详情
    url(r'^xiangqing/$', views.xiangqing, name="xiangqing"),
    # 商品评论
    url(r'^pinglun/$', views.pinglun, name="pinglun"),

    # url(r'^commodity_info/$', views.commodity_info, name='commodity_info')        # 商品信息

<<<<<<< HEAD
    # url(r'^add_cart/$', views.add_cart, name='add_cart'),              # 添加购物车成功页面
    url(r'^my_cart/$', views.my_cart, name='my_cart'),                   # 购物车页面
    url(r'^Personal/$', views.Personal, name='Personal'),                # 个人中心
    url(r'^changeinfo/$', views.changeinfo, name='changeinfo'),          # 修改个人信息
    url(r'^services/$', views.services, name='services'),                # 服务中心
    url(r'^orders/$', views.orders, name='orders'),                      # 订单中心
    url(r'^changepwd/$', views.changepwd, name='changepwd'),             # 修改密码
    url(r'^open_shop/$', views.open_shop, name='open_shop'),             # 申请店铺页面
    url(r'^confirm/$', views.confirm, name='settle'),                    # 确认订单
    url(r'^pay/$', views.pay, name='pay'),                               # 支付
=======
    # url(r'^add_cart/$', views.add_cart, name='add_cart'),                         # 添加购物车成功页面
    url(r'^my_cart/$', views.my_cart, name='my_cart'),                                 # 购物车页面
    url(r'^services/$', views.services, name='services'),                               # 服务中心
    url(r'^orders/$', views.orders, name='orders'),                               # 订单中心

    url(r'^open_shop/$', views.open_shop, name='open_shop'),                        # 申请店铺页面
>>>>>>> cb1b1cda2de65d5dc792e58083aee0740b98fb56

]