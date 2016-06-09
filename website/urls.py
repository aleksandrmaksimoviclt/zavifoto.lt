from django.conf.urls import url, include	
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^contact-us$', views.contact, name='contact-us'),
	url(r'^pricing$', views.pricing, name='pricing'),
	url(r'^about$', views.about, name='about'),
	url(r'^reviews$', views.reviews, name='reviews'),
	url(r'^faq$', views.faq, name='faq'),	

	
	# # projects urls


	# WYSIWYG REDACTOR
	url(r'^redactor/', include('redactor.urls')),

	# Photos sorting
	url(r'^sort/$', views.photosorting, name='photosorting'),
	# url(r'^projects/(?P<name>[-\w]+)/$', views.project),
	# url(r'^(?P<language>[-\w]+)/$', views.change_language)
]