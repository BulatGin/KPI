from django.conf.urls import url, include
from django.contrib import admin

import KPITest

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # TODO  Authorization urls
    #url(r'^auth/$', , name='auth'),
    url(r'', include(KPITest.urls))
]
