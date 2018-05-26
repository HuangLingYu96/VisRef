"""graduationDesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from visualRef import views
from graduationDesign.settings import MEDIA_ROOT
from django.views.static import serve

urlpatterns = [
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    #后台管理
    url(r'^admin/', admin.site.urls),
    #登录
    url(r'^login$',views.mylogin),
    #登出
    url(r'^logout$',views.mylogout),
    #注册
    url(r'^register$',views.register),
    #注册页面ajax，检查用户名占用
    url(r'^check/username$',views.check_username),
    #注册页面ajax，检查邮箱占用
    url(r'^check/email$',views.check_email),
    #忘记密码重置页
    url(r'^password_reset$',views.password_reset),
    #重置页面ajax请求，用于验证用户名和邮箱名
    url(r'^check/user$',views.check_user),

    #home页面
    url(r'^$',views.home),
    #搜索页面
    url(r'^search/$',views.search2),
    #可视化页面
    url(r'^vis/$',views.vis),
    #可视化页面ajax请求，ref可视化
    url(r'^vis/ref$',views.vis_ref),
    #ref可视化详情页
    url(r'^vis/ref/(.+)/$',views.vis_ref_details),
    #ref可视化详情页，分页ajax请求
    url(r'^vis/ref/([^/]+)/([^/]+)/([^/]+)$',views.ref_pagination),
    #可视化页面ajax请求，cit可视化
    url(r'^vis/cit$',views.vis_cit2),
    #cit可视化详情页
    url(r'^vis/cit/(.+)/$',views.vis_cit_details),
    #概要可视化
    url(r'^summary/$',views.summary),

    #个人中心
    #查看收藏
    #url(r'^indiv/([^/]+)/stars/$',views.view_stars),
    #分类别查看收藏
    url(r'^indiv/([^/]+)/stars/([^/]*)$',views.view_stars),
    #删除收藏
    url(r'^dislike$',views.dislike),
    #查看个人信息
    url(r'^indiv/([^/]+)/profile/$',views.view_profile),
    #修改个人信息
    url(r'^profile_modify$',views.profile_modify),
    #修改头像
    url(r'^avatar_modify$',views.avatar),
    #修改密码
    url(r'^indiv/([^/]+)/profile/password_setting$',views.password_setting),
    #修改密码之前，验证原密码
    url(r'^check/password$',views.check_password),
    #修改密码的ajax
    url(r'^password_modify$',views.password_modify),
    #url(r'^indiv/([^/]+)/([^/]+)/$',views.indiv_actice),

    #对应各个界面的收藏动作
    url(r'^star$',views.star),
    url(r'^help/$',views.help)
]
