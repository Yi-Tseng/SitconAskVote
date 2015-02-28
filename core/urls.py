from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'core.views.index'),
    url(r'^about$', 'core.views.about'),
    url(r'^user/', include('users.urls')),
    url(r'^question/', include('question.urls')),
    # facebook
    url(r'^facebook/', include('facebook.urls')),
    #socket io
    url("", include('django_socketio.urls')),
)
