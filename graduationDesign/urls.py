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
    url(r'^admin/', admin.site.urls),
    url(r'^login$',views.mylogin),
    url(r'^logout$',views.mylogout),
    url(r'^register$',views.register),
    url(r'^$',views.home),
    url(r'^search/$',views.search),
    url(r'^vis/$',views.vis),
    url(r'^vis/ref$',views.vis_ref),
    url(r'^vis/ref/(.+)/$',views.vis_ref_details),
    url(r'^vis/cit$',views.vis_cit),
    url(r'^vis/cit/(.+)/$',views.vis_cit_details),
    url(r'^summary/$',views.summary),
    url(r'^indiv/([^/]+)/(.*)/$',views.indiv),
    #url(r'^indiv/([^/]+)/([^/]+)/$',views.indiv_actice),
    url(r'^star$',views.star),
    url(r'^help/$',views.help)
]
