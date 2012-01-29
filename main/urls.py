from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('foos.main.views',
                       url(r'^action/resume_game/$','resume_game'),
                       url(r'^action/win_game/$','win_game'),
                       url(r'^play/$','play_game'),
                       url(r'^action/increment_score/$','increment_score'),
                       url(r'^action/decrement_score/$','decrement_score'),
                       url(r'^action/refresh_score/$','refresh_score'),
                       url(r'^new_game/$','new_game'),
                       url(r'^register/$','register'),
                       url(r'^$','index'))
