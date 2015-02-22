from django.conf.urls import patterns, include, url
import question
import users

urlpatterns = patterns('',
    url(r'^$', 'core.views.index'),
    #url(r'^question/', include(question.urls)),
    #url(r'^user/', include(users.urls)),
)
