from django.conf.urls import patterns, include, url
import question

urlpatterns = patterns('',
    url(r'^question/', include(question.urls)),
)
