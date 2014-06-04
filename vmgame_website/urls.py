from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vmgame_website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^vmgame/', include('vmgame.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
