# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.simple_page.views import HomePage

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='home_page'),
    url(r'^api/', include('apps.api.urls')),
    # url(r'^account/', include('apps.users.urls')),

    url(r'^djangojs/', include('djangojs.urls')),
    url(r'^robots\.txt$', include('robots.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += patterns('',
        url(r'^admin/', include('admin_honeypot.urls')),
        url(r'^admin.php', include('admin_honeypot.urls')),
        url(r'^admin-secret/', include(admin.site.urls)),
    )