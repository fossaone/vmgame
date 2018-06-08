from django.urls import path

from vmgame import views

urlpatterns = [
    path('', views.index, name = 'index'),
# Not sure what the point of this is:
#    path(r'^(?P<vmgame_pick_id>\d+)/$', views.enterpicks, name='enterpicks'),
    path('enterpick/', views.enterpick, name='enterpick'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('mypicks/', views.mypicks, name='mypicks'),
    path('displaypick/<int:pick_id>', views.displaypick, name='displaypick'),
    path('results/', views.results, name='results'),
#    path(r'^results/(?P<pick_id>\w+)$', views.results, name='results_pick'),
    path('logout/', views.user_logout, name='logout'),
    path('scoring/', views.scoring, name='scoring'),
]

