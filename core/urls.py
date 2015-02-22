from django.conf.urls import patterns, include, url
import question
import users

urlpatterns = patterns('',
    url(r'^$', 'core.views.index'),
    url(r'^about$', 'core.views.about'),
    url(r'^user/', include(users.urls)),
    #url(r'^question/', include(question.urls)),
    
)
