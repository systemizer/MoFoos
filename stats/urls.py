from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('foos.stats.views',
                       url(r'^view/outcome/','view_outcome'),
                       url(r'^view/team/','view_team'),
                       url(r'^view/profile/','view_profile'),
                       url(r'^edit/team/','edit_team'),
                       url(r'^edit/profile/','edit_profile'),

                       url(r'^$','index'))


