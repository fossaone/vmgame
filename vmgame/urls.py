from django.conf.urls import patterns, url

from vmgame import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    #url(r'^(?P<vmgame_pick_id>\d+)/$', views.enterpicks, name='enterpicks'),
    url(r'^enterpicks/', views.enterpicks, name='enterpicks'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^displaypicks/(?P<displaypick_name_url>\w+)/$', views.displaypick, name='displaypick'),
    url(r'^displaypicks/$', views.displaypicks, name='displaypicks'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
)
