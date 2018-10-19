from django.conf.urls import  url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),                                       # 主页
    url(r'^index/$', views.index, name='index'),                                  # 主页

    # url(r'^register/$', views.register, name='register'),                         # 注册
    # url(r'^login/$', views.login, name='login'),                                  # 登录

    # url(r'^commodity_info/$', views.commodity_info, name='commodity_info')        # 商品信息

    # url(r'^add_cart/$', views.add_cart, name='add_cart'),                         # 添加购物车成功页面
    url(r'^cart/$', views.my_cart, name='login'),                                 # 购物车页面

]