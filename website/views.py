
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required


from .models import *
from .utils import get_ordered_photos


def index(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)
    try:
        seo = IndexPage.objects.get(language=language).indexpage_seo_set.first()
    except:
        seo = []
    if pagesettings.layout == 0:
        template = 'website/index_grid.html'
        try:
            photos = Photo.objects.filter(is_for_index_grid=True)
        except:
            photos = []
    if pagesettings.layout == 1:
        template = 'website/index_slider.html'
        try:
            photos = Photo.objects.filter(is_for_index_slider=True)
        except:
            photos = []

    response = render(
        request,
        template,
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
            'pagesettings': pagesettings,
            'photos': photos,
            'seo': seo,
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

    try:
        seo = RetouchPage.objects.get(language=language).retouchpage_seo_set.first()
    except:
        seo = []

    response = render(
        request,
        'website/retouch.html', {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'galleries': data,
            'comparisonphotos': comparisonphotos,
            'pagesettings': pagesettings,
            'seo': seo,
        })
    return response


def category(request, gallery_slug, category_slug):

    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        category = CategoryByLanguage.objects.filter(
            language=language,
            url=category_slug,).first().category.photos_order
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

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        context['galleries'] = Gallery.objects.all()
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        _type = request.POST.get('type')
        _id = request.POST.get('id')
        print(_type)
        if _type == 'gallery':
            gallery = Gallery.objects.get(id=_id)
            for file in request.FILES.getlist('files'):
                Photo.objects.create(name=file.name, image=file, gallery=gallery)

        elif _type == 'category':
            _category = Category.objects.get(id=_id)
            for file in request.FILES.getlist('files'):
                _photo = Photo.objects.create(name=file.name, image=file)
                test = PhotoCategory.objects.create(category=_category, photo=_photo)
                print(_category, _photo)
                print(test)
        else:
            HttpResponse('No such type: {}'.format(_type))

        return HttpResponse('Done!')


def contact(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = ContactsPage.objects.get(language=language).contactspage_seo_set.first()
    except:
        seo = []

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
            'seo': seo,
        })
    return response


def pricing(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = PricePage.objects.get(language=language).pricepage_seo_set.first()
    except:
        seo = []

    try:
        pricepage = PricePage.objects.filter(language=language).first()

    except Exception:
        pricepage = []

    try:
        questions = Question.objects.filter(pricepage=pricepage.id).first()

    except Exception:
        questions = []

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
            'seo': seo,
        })
    return response

def about(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = AboutPage.objects.get(language=language).aboutpage_seo_set.first()
    except:
        seo = []

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
            'seo': seo,
        })
    return response


def reviews(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = ReviewPage.objects.get(language=language).reviewpage_seo_set.first()
    except:
        seo = []

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
            'seo': seo,
        })
    return response


def faq(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = FaqPage.objects.get(language=language).faqpage_seo_set.first()
    except:
        seo = []

    try:
        faqpage = FaqPage.objects.filter(language=language).first()

    except Exception:
        faqpage = []

    try:
        questions = Question_FaqPage.objects.filter(faqpage=faqpage.id).first()

    except Exception:
        questions = []

    try:
        photos = Photo.objects.filter(is_for_faq_page_side=True)
    except:
        photos = []

    response = render(
        request,
        'website/faq.html',
        {
            'current_language': language.language_code,
            'available_languages': available_languages,
            'faqpage': faqpage,
            'questions': questions,
            'galleries': data,
            'photos': photos,
            'pagesettings': pagesettings,
            'seo': seo,
        })
    return response


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