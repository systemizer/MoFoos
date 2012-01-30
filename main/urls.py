from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('foos.main.views',
                       url(r'^make_team/$','make_team'),
                       url(r'^action/increment_score/$','increment_score'),
                       url(r'^action/decrement_score/$','decrement_score'),
                       url(r'^action/end_game/$','end_game'),
                       url(r'^action/refresh_score/$','refresh_score'),
                       url(r'^new_game/$','new_game'),

                       url(r'^register/$','register'),
                       url(r'^login/$','login'),
                       url(r'^$','index'))
