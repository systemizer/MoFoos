from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('foos.stats.views',
                       url(r'^view/outcome/','view_outcome'),
                       url(r'^view/team/','view_team'),
                       url(r'^profile/','profile'),

                       url(r'^$','index'))


