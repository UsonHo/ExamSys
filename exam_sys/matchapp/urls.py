"""exam_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from matchapp import views

app_name = 'matchapp'

urlpatterns = [
    url(r'^setgame/$', views.set_game, name='match_config'),
    url(r'^info_(?P<mid>\d+)/$', views.matchinfo, name='info'),
    url(r'^detail_(?P<mid>\d+)_(?P<tokencode>\w+)/', views.matchdetail, name='exam'),

    re_path('rank/(?P<mid>\d+)/', views.matchrank, name='rank'),
    re_path('result/(?P<mid>\d+)/', views.matchresult, name='result'),

    url(r'^list/$', views.matchlist, name='list'),  # 已被代替
    url(r'^list_del/(?P<mid>\d+)/$', views.matchlist_del, name='list_del'),

    url(r'^match_list/(?P<qid>\d+)/', views.match_list, name='match_list'),
]
