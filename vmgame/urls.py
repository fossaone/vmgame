from django.conf.urls import patterns, url

from vmgame import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    #url(r'^(?P<vmgame_pick_id>\d+)/$', views.enterpicks, name='enterpicks'),
    #url(r'^enterpicks/', views.enterpicks, name='enterpicks'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^displaypicks/$', views.displaypicks, name='displaypicks'),
    url(r'^displaypicks/(?P<user_pick_id>\w+)$', views.displaypicks, name='display_user_pick'),
    url(r'^results/$', views.results, name='results'),
    url(r'^results/(?P<pick_id>\w+)$', views.results, name='results_pick'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
)
