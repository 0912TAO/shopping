from django.conf.urls import  url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),                                       # 主页
    url(r'^index/$', views.index, name='index'),                                  # 主页
    url(r'^code/$', views.code, name='code'),
    url(r'^register/$', views.register, name='register'),                         # 注册
    url(r'^user_login/$', views.user_login, name='user_login'),                                  # 登录
    # 验证验证码
    url(r'^(\w+)/checkcode/$', views.checkcode, name='checkcode'),
    # 验证用户名是否存在
    url(r'^(\w+)/checkusername/$', views.checkusername, name='checkusername'),
    # 退出登录
    url(r'^user_logout/$', views.user_logout, name="user_logout"),
    # 修改用户头像
    url(r'^change_header/$', views.change_header, name="change_header"),
    # 修改用户密码
    url(r'^change_password/$', views.change_password, name="change_password"),
    # 商品购买
    url(r'^product/$', views.product, name="product"),
    # 商品详情
    url(r'^xiangqing/$', views.xiangqing, name="xiangqing"),
    # 商品评论
    url(r'^pinglun/$', views.pinglun, name="pinglun"),

    # url(r'^commodity_info/$', views.commodity_info, name='commodity_info')        # 商品信息

    # url(r'^add_cart/$', views.add_cart, name='add_cart'),                         # 添加购物车成功页面
    url(r'^my_cart/$', views.my_cart, name='my_cart'),                                 # 购物车页面

]