from django.conf.urls import url
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

	# url(r'^projects/(?P<name>[-\w]+)/$', views.project),
	# url(r'^(?P<language>[-\w]+)/$', views.change_language)
]