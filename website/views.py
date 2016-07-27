import ast

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import get_ordered_photos # va sitai siusk belekuri photos_order attr


def index(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)
    galleries = GalleryByLanguage.objects.filter(
        language=language).select_related(
        'gallery__category').prefetch_related(
        'gallery__category__categorybylanguage_set')
    data = []
    for gallery in galleries:
        data.append({
            'name': gallery.name,
            'categories': [{
                'name': cat.name,
                'url': cat.url} for cat in gallery.gallery.category.categorybylanguage_set.filter(language=language)]
        })
    response = render(
        request,
        'website/index.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
        })
    return response


def retouch(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    galleries = GalleryByLanguage.objects.filter(
        language=language).select_related(
        'gallery__category').prefetch_related(
        'gallery__category__categorybylanguage_set')

    data = []

    for gallery in galleries:
        data.append(
            {
                'name': gallery.name,
                'categories': [{
                    'name': cat.name,
                    'url': cat.url} for cat in gallery.gallery.category.categorybylanguage_set.filter(language=language)]
            })

    response = render(
        request,
        'website/retouch.html', {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
        })
    return response


def category(request, gallery_slug, category_slug):

    available_languages = Language.objects.all()
    language = get_language_obj(request)

    response = render(
        request,
        'website/category.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,

        })

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


def contact(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    try:
        contactspage = ContactsPage.objects.filter(language=language).first()

    except Exception:
        contactspage = []

    response = render(
        request,
        'website/contact-us.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'contactspage': contactspage,
        })
    return response


def pricing(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    try:
        pricepage = PricePage.objects.filter(language=language).first()

    except Exception:
        pricepage = []

    try:
        questions = Question.objects.filter(pricepage=pricepage.id)

    except Exception:
        question = []

    response = render(
        request,
        'website/pricing.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'pricepage': pricepage,
            'questions': questions,
        })
    return response


def about(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    try:
        aboutpage = AboutPage.objects.filter(language=language).first()

    except Exception:
        aboutpage = []

    response = render(
        request,
        'website/about.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'aboutpage': aboutpage,
        })
    return response


def reviews(request):
    reviews = Review.objects.all()
    response = render(
        request,
        'website/reviews.html', {'reviews': reviews})
    return response


def faq(request):
    response = render(
        request,
        'website/faq.html')
    return response


def photosorting(request):
    categories = CategoryByLanguage.objects.filter(language__language='lt')

    response = render(
        request, 'website/photosorting.html',
        {'categories': categories})

    return response


def categorysorting(request, category_id):

    categories = CategoryByLanguage.objects.filter(
        language__language='lt', id=category_id,)
    galleries = Gallery.objects.filter(category=categories[0].category)
    galleries_lang = GalleryByLanguage.objects.filter(gallery__in=galleries)

    response = render(
        request, 'website/photosorting.html',
        {
            'categories': categories,
            'galleries': galleries,
            'galleries_lang': galleries_lang
        })

    return response


def galleriessorting(request, gallery_id):

    gallery = Gallery.objects.get(id=gallery_id)

    response = render(
        request, 'website/photosorting.html',
        {'gallery': gallery, 'type': 'gallery'}
        )
    return response


@csrf_exempt
def change_order(request):
    json = request.read()
    data = ast.literal_eval(json.decode("utf-8"))
    if data['type'] == 'gallery':
        model = Gallery
    elif data['type'] == 'category':
        model = Category

    obj = model.objects.get(id=data['id'])
    obj.photos_order = data['order']
    obj.save()
    return HttpResponse('Changed')


def get_language_obj(request):
    available_langs = [l.language_code for l in Language.objects.all()]
    try:
        lang = request.COOKIES['language']
    except Exception:
        lang = DEFAULT_LANGUAGE
    if lang not in available_langs:
        lang = DEFAULT_LANGUAGE
    return Language.objects.get(language_code=lang)


def change_language(request, language):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(key='language', value=language)
    return response
