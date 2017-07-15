from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

import KPITest
import auth
from KPI import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('auth.urls'), name='auth'),
    url(r'', include('KPITest.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
