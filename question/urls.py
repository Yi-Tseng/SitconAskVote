from django.conf.urls import patterns, url
from question import views
urlpatterns = patterns('',
    url(r'^ask$', views.ask),
    url(r'^view$', views.view_question),
    url(r'^want$', views.want_listen),
)
