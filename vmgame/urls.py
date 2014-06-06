from django.conf.urls import patterns, url

from vmgame import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    #url(r'^(?P<vmgame_pick_id>\d+)/$', views.enterpicks, name='enterpicks'),
    url(r'^enterpicks/', views.enterpicks, name='enterpicks'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
)
