from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'painel.views.select'),
    url(r'^painel/', include('painel.urls')),

)
