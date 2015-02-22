from django.conf.urls import patterns, url
from users import views
urlpatterns = patterns(
    '',
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
)