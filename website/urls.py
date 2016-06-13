from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'upload/', views.UploadView.as_view()),
	url(r'^change-order$', views.change_order, name='change-order'),
	# url(r'^about$', views.about, name='about'),
	# url(r'^contact-us$', views.contact, name='contact-us'),
	# url(r'^projects/$', views.projects, name='projects'),
	
	# # projects urls

	# url(r'^projects/(?P<name>[-\w]+)/$', views.project),
	# url(r'^(?P<language>[-\w]+)/$', views.change_language)
]
urlpatterns.append(url(r'^plate/', include('django_spaghetti.urls')))