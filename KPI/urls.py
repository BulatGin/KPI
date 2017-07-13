from django.conf.urls import url, include
from django.contrib import admin

import KPITest
import auth

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # TODO  Authorization urls
    url(r'^auth/', include('auth.urls'), name='auth'),
    url(r'', include('KPITest.urls'))
]
