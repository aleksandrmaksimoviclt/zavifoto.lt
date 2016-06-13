from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Photo, Gallery, Category


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

def change_order(request):
	type = request.POST.get('type')
	if type == 'gallery':
		model = Gallery
	elif type == 'category':
		model = Category

	obj = model.objects.get(id=request.POST.get('id'))
	obj.photos_order = request.POST.get('order')
	return HttpResponse('Changed')