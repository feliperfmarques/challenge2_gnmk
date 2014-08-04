from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'challenge2_gnmk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'painel.views.select'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'painel/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/painel/login/'}),
    url(r'^select/$', 'painel.views.select'),
    url(r'^references/$', 'painel.views.references'),
    url(r'^history/$', 'painel.views.history'),
    url(r'^download/(?P<filename>[a-zA-Z0-9_.-]+)/$', 'painel.views.download'),
    url(r'^delete/(?P<filename>[a-zA-Z0-9_.-]+)/$', 'painel.views.delete'),

)
