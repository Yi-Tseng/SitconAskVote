from django.conf.urls import patterns, url
from question import views
urlpatterns = patterns('',
    url(r'^$', views.view_question),
    url(r'^ask$', views.ask),
    url(r'^view$', views.view_question),
    url(r'^want$', views.want_listen),
    url(r'^edit$', views.edit),
    url(r'^del$', views.delete),
    url(r'^solve$', views.solve),
    url(r'^unsolve$', views.unsolve),
    url(r'^live$', views.live_view),
    url(r'^current_live$', views.get_current_live_question),
    url(r'^set_live$', views.set_live),
    
)
