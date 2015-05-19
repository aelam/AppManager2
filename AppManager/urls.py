from django.conf.urls import patterns, include, url
from django.contrib import admin
from AppManager import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'AppManager.views.home', name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('Application.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
