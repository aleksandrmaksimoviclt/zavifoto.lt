
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Change language
    url(r'^set-language/(?P<language>[-\w]+)$', views.change_language), 

    url(r'^contact-us$', views.contact, name='contact-us'),
    url(r'^pricing$', views.pricing, name='pricing'),
    url(r'^about$', views.about, name='about'),
    url(r'^reviews$', views.reviews, name='reviews'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^retouch$', views.retouch, name='retouch'),
    url(r'^(?P<gallery_slug>[-\w]+)/(?P<category_slug>[-\w]+)$', views.category),

    url(r'upload/', views.UploadView.as_view()),

    # URL FOR WYSIWYG REDACTOR
    url(r'^redactor/', include('redactor.urls')),
]
