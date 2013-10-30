from django.conf.urls import patterns, include
from django.contrib import admin
from oscar.app import shop


admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include(shop.urls)),
)
