__author__ = 'ryan'

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('Application.views',
    url(r'^$', 'app_list', name="apps"),
    url(r"^(?P<app_id>\d+)/$", 'app_detail', name="app-detail"),
    url(r'^package/(?P<id>\d+)/$', 'app_packages_list'),
    url(r"^install/", "ota_plist", name="app-install"),
    url(r"^upload/", "package_upload"),
    url(r'^package/save/$', 'package_update'),
    url(r'^provs/$', 'provisioning_profile_list'),
    url(r"^appstore", "appstore"),
    url(r"^prepare", "prepare"),
)

