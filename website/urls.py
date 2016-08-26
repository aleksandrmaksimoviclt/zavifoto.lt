
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Change language
    url(r'^set-language/(?P<language>[-\w]+)$', views.change_language), 
    # LT URLS
    url(r'^kontaktai$', views.contact, name='contacts-lt'),
    url(r'^kainos$', views.pricing, name='pricing-lt'),
    url(r'^apie-mus$', views.about, name='about-lt'),
    url(r'^atsiliepimai$', views.reviews, name='reviews-lt'),
    url(r'^duk$', views.faq, name='faq-lt'),
    url(r'^retusavimas$', views.retouch, name='retouch-lt'),

    # EN URLS
    url(r'^contact-us$', views.contact, name='contacts-en'),
    url(r'^pricing$', views.pricing, name='pricing-en'),
    url(r'^about$', views.about, name='about-en'),
    url(r'^reviews$', views.reviews, name='reviews-en'),
    url(r'^faq$', views.faq, name='faq-en'),
    url(r'^retouch$', views.retouch, name='retouch-en'),

    # ru URLS
    url(r'^kontakty$', views.contact, name='contacts-ru'),
    url(r'^ceny$', views.pricing, name='pricing-ru'),
    url(r'^o-nas$', views.about, name='about-ru'),
    url(r'^otzyvy$', views.reviews, name='reviews-ru'),
    url(r'^chavo$', views.faq, name='faq-ru'),
    url(r'^retushirovanie$', views.retouch, name='retouch-ru'),
    url(r'^(?P<category_slug>[-\w]+)$', views.category),
    url(r'^(?P<category_slug>[-\w]+)/(?P<gallery_slug>[-\w]+)$', views.gallery),

    url(r'upload/', views.UploadView.as_view()),

    # URL FOR WYSIWYG REDACTOR
    url(r'^redactor/', include('redactor.urls')),
]
