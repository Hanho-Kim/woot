from django.conf.urls import include, url

from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = [

    #url(r'^admin/', include(admin.site.urls)),
    url('', include('underbarApp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
