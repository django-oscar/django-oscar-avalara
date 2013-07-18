from django.conf.urls.defaults import *
from django.contrib import admin
from apps.app import shop


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include(shop.urls)),
)
