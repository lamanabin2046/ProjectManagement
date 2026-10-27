# vehicleManagement/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Accounts/', include('accounts.urls')),
    path('Projects/', include('projects.urls')),
    path('UserCommittee/', include('usercommittee.urls')),
    path('Bidding/', include('biddings.urls')),
    path('Quatation/', include('quatation.urls')),
    path('Letters/', include('letters.urls')),
    path('', RedirectView.as_view(url='/Accounts/login/', permanent=False)),
]






if settings.DEBUG:
    from django.http import Http404
    from django.urls import re_path

    def _private_media(request, *args, **kwargs):
        raise Http404  # सदस्यका कागजात: /UserCommittee/Person/<id>/doc/<kind>/ (अनुमति जाँचेर) मात्र

    urlpatterns += [re_path(r"^media/[^/]+/persons/", _private_media)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)