
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

    # it URLS
    url(r'^contatti$', views.contact, name='contacts-it'),
    url(r'^prezzi$', views.pricing, name='pricing-it'),
    url(r'^chi-siamo$', views.about, name='about-it'),
    url(r'^referenze$', views.reviews, name='reviews-it'),
    url(r'^faq-it$', views.faq, name='faq-it'),
    url(r'^fotoritocco$', views.retouch, name='retouch-it'),


    # Category
    url(r'^(?P<category_slug>[-\w]+)$', views.category),

    # Gallery
    url(r'^(?P<category_slug>[-\w]+)/(?P<gallery_slug>[-\w]+)$', views.gallery),

    url(r'upload/', views.UploadView.as_view()),

    # URL FOR WYSIWYG REDACTOR
    url(r'^redactor/', include('redactor.urls')),
]
