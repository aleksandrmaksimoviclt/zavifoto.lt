import ast

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import *
from .utils import get_ordered_photos

def index(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    response = render(
        request,
        'website/index.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
            'pagesettings': pagesettings,
        })
    return response


def retouch(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        comparisonphotos = ComparisonPhoto.objects.all()
    except:
        comparisonphotos = []

    response = render(
        request,
        'website/retouch.html', {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
            'comparisonphotos': comparisonphotos,
            'pagesettings': pagesettings,
        })
    return response


def category(request, gallery_slug, category_slug):

    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try: 
        category = CategoryByLanguage.objects.filter(language=language, url=category_slug,).first().category.photos_order
    except:
        category = []

    try:
        category_photos = get_ordered_photos(photos_order=category)
    except:
        category_photos = []

    response = render(
        request,
        'website/category.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
            'photos': category_photos,
            'pagesettings': pagesettings,

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

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        contactspage = ContactsPage.objects.filter(language=language).first()

    except Exception:
        contactspage = []

    try:
        photos = Photo.objects.filter(is_for_price_page_side=True)
    except:
        photos = []

    response = render(
        request,
        'website/contact-us.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'contactspage': contactspage,
            'galleries': data,
            'photos': photos,
            'pagesettings': pagesettings,
        })
    return response


def pricing(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        pricepage = PricePage.objects.filter(language=language).first()

    except Exception:
        pricepage = []

    try:
        questions = Question.objects.filter(pricepage=pricepage.id)

    except Exception:
        question = []

    try:
        photos = Photo.objects.filter(is_for_price_page_side=True)
    except:
        photos = []

    response = render(
        request,
        'website/pricing.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'pricepage': pricepage,
            'questions': questions,
            'galleries': data,
            'photos': photos,
            'pagesettings': pagesettings,
        })
    return response


def about(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        aboutpage = AboutPage.objects.filter(language=language).first()

    except Exception:
        aboutpage = []

    try:
        photos = Photo.objects.filter(is_for_about_us_page_side=True)
    except:
        photos = []

    response = render(
        request,
        'website/about.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'aboutpage': aboutpage,
            'galleries': data,
            'photos': photos,
            'pagesettings': pagesettings,
        })
    return response


def reviews(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    reviews = Review.objects.all()

    try:
        photos = Photo.objects.filter(is_for_review_page_side=True)
    except:
        photos = []

    response = render(
        request,
        'website/reviews.html', {
        'reviews': reviews,
        'current_language': language.language_code,
        'available_languages': available_languages,
        'galleries': data,
        'photos': photos,
        'pagesettings': pagesettings,
        })
    return response


def faq(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        photos = Photo.objects.filter(is_for_faq_page_side=True)
    except:
        photos = []

    response = render(
        request,
        'website/faq.html',{
        'current_language': language.language_code,
        'available_languages': available_languages,
        'galleries': data,
        'photos': photos,
        'pagesettings': pagesettings,
        })
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
    category = categories.first().category
    photos = get_ordered_photos(category.photos_order)
    galleries = Gallery.objects.filter(category=categories[0].category)
    galleries_lang = GalleryByLanguage.objects.filter(gallery__in=galleries)

    response = render(
        request, 'website/photosorting.html',
        {
            'categories': categories,
            'galleries': galleries,
            'galleries_lang': galleries_lang,
            'category': category,
            'photos': photos,
            'type': 'category',
        })

    return response


def galleriessorting(request, gallery_id):

    gallery = Gallery.objects.get(id=gallery_id)
    photos = get_ordered_photos(gallery.photos_order)
    response = render(
        request, 'website/photosorting.html',
        {'gallery': gallery, 'type': 'gallery', 'photos': photos}
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
    else:
        return HttpResponse('Something went wrong')

    obj = model.objects.get(id=data['id'])
    obj.photos_order = data['order']
    obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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

def retrieve_sidemenu_galleries(request, language):

    try:

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
    except:

        data = []
        galleries = []

    return data