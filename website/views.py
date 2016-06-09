from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import *



def set_language(language):
	try:
		language = Language.objects.get(language_code=language).id
	except Exception as e:
		language = Language.objects.get(language_code='lt').id
	return language

def index(request):
	response = render(
		request,
		'website/index.html')
	return response

class UploadView(TemplateView):

	template_name = 'website/upload.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(UploadView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(UploadView, self).get_context_data(**kwargs)
		context['galleries'] = Gallery.objects.all()
		return context

	def post(self, request, *args, **kwargs):
		gallery_id = request.POST.get('gallery')
		gallery = Gallery.objects.get(id=gallery_id)
		for file in request.FILES.getlist('files'):
			Photo.objects.create(name=file.name, image=file, gallery=gallery)

		return HttpResponse('Done!')

def contact (request):
	
	response = render(
		request,
		'website/contact-us.html')
	return response

def pricing(request):
	response = render(
		request,
		'website/pricing.html')
	return response

def about(request):
	response = render(
		request,
		'website/about.html')
	return response

def reviews(request):
	reviews = Review.objects.all()
	response = render(
		request,
		'website/reviews.html', {'reviews' : reviews,})
	return response

def faq(request):
	response = render(
		request,
		'website/faq.html')
	return response