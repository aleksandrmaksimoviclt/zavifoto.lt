from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sort/', include('sorting.urls')),
    url(r'^', include('website.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns(
        '', url(r'^plate/', include('django_spaghetti.urls')),
    )
# Change admin site title
admin.site.site_header = _("zavifoto.lt administration")
admin.site.site_title = _("Zavifoto.lt")
