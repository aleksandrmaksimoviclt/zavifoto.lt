from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

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
	response = render(
		request,
		'website/reviews.html')
	return response

def faq(request):
	response = render(
		request,
		'website/faq.html')
	return response