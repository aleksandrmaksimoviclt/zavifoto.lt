
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

    # make queries for every created page object to get menu name field and show it in menu
    # use as example retrieve sidemenu galeries function

    try:
        seo = IndexPageSeo.get(language=language).first()
    except:
        seo = []

    if pagesettings.layout == 0:
        template = 'website/index_grid.html'
        photos = Photo.objects.filter(is_for_index_grid=True)

    if pagesettings.layout == 1:
        template = 'website/index_slider.html'
        photos = Photo.objects.filter(is_for_index_slider=True)

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
        seo = RetouchPage.objects.get(
            language=language).retouchpage_seo_set.first()
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
        files = request.FILES.getlist('files')
        if not files:
            return render(request, 'website/upload.html', {'danger': 'No photos selected!'})

        if _type == 'gallery':
            _gallery = Gallery.objects.filter(id=_id)
            if _gallery.exists():
                _gallery = _gallery.first()
                for file in files:
                    _photo = Photo.objects.create(name=file.name, image=file)
                    GalleryPhoto.objects.create(photo=_photo, gallery=_gallery)

        elif _type == 'category':
            _category = Category.objects.filter(id=_id)
            if _category.exists():
                _category = _category.first()
                for file in files:
                    _photo = Photo.objects.create(name=file.name, image=file)
                    PhotoCategory.objects.create(
                        category=_category, photo=_photo)
        else:
            for file in files:
                Photo.objects.create(name=file.name, image=file)

        return render(request, 'website/upload.html', {'success': 'Done!'})


def contact(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = ContactsPageSeo.objects.get(language=language).first()
    except:
        seo = []

    try:
        contactspage = ContactsPageByLanguage.objects.filter(language=language).first()

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
        seo = PricePageSeo.objects.get(language=language).first()
    except:
        seo = []

    try:
        pricepage = PricePageByLanguage.objects.filter(language=language).first()

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
        seo = AboutPageSeo.objects.get(language=language).first()
    except:
        seo = []

    try:
        aboutpage = AboutPageByLanguage.objects.filter(language=language).first()

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
        reviewpage = ReviewPageByLanguage.objects.get(language=language)
    except:
        reviewpage = []
    try:
        seo = ReviewPageSeo.objects.get(language=language).first()
    except:
        seo = []

    try:
        reviews = ReviewByLanguage.objects.filter(language=language)
    except:
        reviews = []
    try:
        photos = ReviewPagePhoto.objects.filter(is_side_photo=True)
    except:
        photos = []

    response = render(
        request,
        'website/reviews.html', {
            'reviews': reviews,
            'reviewpage': reviewpage,
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
        seo = FaqPageSeo.objects.get(language=language).first()
    except:
        seo = []

    try:
        faqpage = FaqPageByLanguage.objects.filter(language=language).first()

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
