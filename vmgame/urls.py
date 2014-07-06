from django.conf.urls import patterns, url

from vmgame import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
# Not sure what the point of this is:
#    url(r'^(?P<vmgame_pick_id>\d+)/$', views.enterpicks, name='enterpicks'),
    url(r'^enterpick/', views.enterpick, name='enterpick'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^mypicks/$', views.mypicks, name='mypicks'),
    url(r'^displaypick/(?P<pick_id>\w+)$', views.displaypick, name='displaypick'),
    url(r'^results/$', views.results, name='results'),
#    url(r'^results/(?P<pick_id>\w+)$', views.results, name='results_pick'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^scoring/$', views.scoring, name='scoring'),

)
