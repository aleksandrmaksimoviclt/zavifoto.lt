from django.conf.urls import url, include	
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

	# Change language
	url(r'^set-language/(?P<language>[-\w]+)/$', views.change_language), 

	url(r'^contact-us$', views.contact, name='contact-us'),
	url(r'^pricing$', views.pricing, name='pricing'),
	url(r'^about$', views.about, name='about'),
	url(r'^reviews$', views.reviews, name='reviews'),
	url(r'^faq$', views.faq, name='faq'),
	url(r'^(?P<gallery_slug>[-\w]+)/(?P<category_slug>[-\w]+)/$', views.category),

	url(r'upload/', views.UploadView.as_view()),
	url(r'^change-order$', views.change_order, name='change-order'),

	# URL FOR WYSIWYG REDACTOR
	url(r'^redactor/', include('redactor.urls')),

	# Photos sorting
	url(r'^sort/$', views.photosorting, name='photosorting'),
	url(r'^sort/(?P<category_id>\w+)/category/$', views.categorysorting),
	url(r'^sort/(?P<gallery_id>\w+)/gallery/$', views.galleriessorting),
	# url(r'^projects/(?P<name>[-\w]+)/$', views.project),
	# url(r'^(?P<language>[-\w]+)/$', views.change_language)
]
urlpatterns.append(url(r'^plate/', include('django_spaghetti.urls')))