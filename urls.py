from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('foos.main.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/',include('django.contrib.auth.urls'))
)

urlpatterns+=staticfiles_urlpatterns()
