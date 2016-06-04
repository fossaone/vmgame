from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vmgame_website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^emgame/', include('vmgame.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #Re-direct from root to emgame
    url(r'^$', RedirectView.as_view(url='emgame/', permanent=False), name='index'),
)
