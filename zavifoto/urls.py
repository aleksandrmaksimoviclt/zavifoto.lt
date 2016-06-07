from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from zavifoto import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('website.urls')),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()