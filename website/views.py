from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe


from .models import *
from .utils import get_ordered_photos
from .forms import ContactForm
from mail.email import EmailSend


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

    if pagesettings.layout == 1:
        template = 'website/index/slider/slider.html'

    elif pagesettings.layout == 2:
        template = 'website/index/grid/grid_2_x_*.html'

    elif pagesettings.layout == 3:
        template = 'website/index/grid/grid_3_x_*.html'

    elif pagesettings.layout == 4:
        template = 'website/index/grid/grid_4_x_*.html'

    elif pagesettings.layout == 5:
        template = 'website/index/grid/grid_5_x_*.html'

    elif pagesettings.layout == 6:
        template = 'website/index/grid/grid_6_x_*.html'


    page = IndexPage.objects.filter()
    if page.exists():
        photos = get_ordered_photos(page.first().photos_order)
    else:
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


def gallery(request, gallery_slug, category_slug):
    if request.method == 'POST':
        try:
            CategoryByLanguage.obejcts.get(url=category_slug)
            gallery = GalleryByLanguage.objects.get(
                url=gallery_slug).gallery.photos_order
        except CategoryByLanguage.DoesNotExist:
            return HttpResponseRedirect('/')

        except GalleryByLanguage.DoesNotExist:
            return HttpResponseRedirect('/')

        gallery_photos = get_ordered_photos(gallery.gallery.photos_order)
        html = """
            <div class="slider-wrapper">
                <div id="slider" class="flexslider">
                    <ul class="slides">
            """
        for photo in gallery_photos:
                html += """
                        <li class="slide-image-wrapper">
                            <img class="imgcover" src="{}"/>
                        </li>
                        """.format(photo["src"])
        html += """
                        </ul>
                    </div>
                <div id="carousel" class="flexslider">
                    <ul class="slides">
                    """
        for photo in category_photos:
            html += """
                    <li class="slide-image-wrapper">
                        <img class="imgcover" src="{}"/>
                    </li>
                    """.format(photo["src"])
        html += """
                            </ul>
                        </div>
                    </div>
                """
    else:
        try:
            CategoryByLanguage.obejcts.get(url=category_slug)
            gallery = GalleryByLanguage.objects.get(
                url=gallery_slug).gallery.photos_order
        except CategoryByLanguage.DoesNotExist:
            return HttpResponseRedirect('/')

        except GalleryByLanguage.DoesNotExist:
            return HttpResponseRedirect('/')

        available_languages = Language.objects.all()
        language = get_language_obj(request)

        pagesettings = PageSettings.objects.first()

        if pagesettings.layout == 1:
            template = 'website/category/slider/slider.html'
        else:
            template = 'website/category/grid/grid_{}_x_*.html'.format(pagesettings.layout)

        data = retrieve_sidemenu_galleries(request, language=language)
        gallery_photos = get_ordered_photos(gallery.gallery.photos_order)

        response = render(
            request,
            template,
            {
                'current_language': language.language_code,
                'available_languages': available_languages,
                'galleries': data,
                'photos': gallery_photos,
                'pagesettings': pagesettings,

            })
        return response
        


def category(request, category_slug):
    if request.method == 'POST':
        pagesettings = PageSettings.objects.first()
        layout = pagesettings.layout

        if layout == 2:
            layout = 'col-xs-6'
        elif layout == 3:
            layout = 'col-xs-4'
        elif layout == 4:
            layout = 'col-xs-3'
        elif layout == 5:
            layout = 'col-xs-12_5'
        elif layout == 6:
            layout = 'col-xs-2'

        if layout != 1:
            categorybylanguage = CategoryByLanguage.objects.get(url=category_slug)    
            category_photos = []
            _counter = 0
            for _gallery in categorybylanguage.category.gallery_set.all():
                _counter += 1
                gallery_photo_order = _gallery.photos_order
                photos = get_ordered_photos(gallery_photo_order)

                for photo in photos:
                    photo.update({'gallery': _counter})

                category_photos += photos
            
            html ='''
            <div class="demo-gallery">
                <ul id="lightgallery" class="filtr-container list-unstyled marginbottom0">
            '''
            for photo in category_photos:
                html += '''
                <li class="{0} grid nopadding filtr-item" data-category="{2}" data-src="{1}">
                    <img href="" class="imgcover grid" src="{1}">
                </li>
                '''.format(layout, photo['src'], photo['gallery'],)

            html += '''
                </ul>
            </div>
            '''
        else:
            html = """
            <div class="slider-wrapper">
                <div id="slider" class="flexslider">
                    <ul class="slides">
            """
            for photo in category_photos:
                html += """
                        <li class="slide-image-wrapper">
                            <img class="imgcover" src="{}"/>
                        </li>
                        """.format(photo["src"])
            html += """
                        </ul>
                    </div>
                <div id="carousel" class="flexslider">
                    <ul class="slides">
                    """
            for photo in category_photos:
                html += """
                    <li class="slide-image-wrapper">
                        <img class="imgcover" src="{}"/>
                    </li>
                    """.format(photo["src"])
            html += """
                            </ul>
                        </div>
                    </div>
                """
        return HttpResponse(html)

    else:
        try:
            category = CategoryByLanguage.objects.get(url=category_slug)
        except CategoryByLanguage.DoesNotExist:
            return HttpResponseRedirect('/')

        available_languages = Language.objects.all()
        language = get_language_obj(request)

        pagesettings = PageSettings.objects.first()

        if pagesettings.layout == 1:
            template = 'website/category/slider/slider.html'
        else:
            template = 'website/category/grid/grid_{}_x_*.html'.format(pagesettings.layout)

        data = retrieve_sidemenu_galleries(request, language=language)
        
        category_photos = []
        _galleriesbylanguage = category.category.gallery_set.all()
        for _gallerybylanguage in _galleriesbylanguage:
            gallery_photo_order = _gallerybylanguage.photos_order
            category_photos += (get_ordered_photos(gallery_photo_order))

        response = render(
            request,
            template,
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
        data = {
            'galleries': Gallery.objects.all(),
            'categories': Category.objects.all(),
        }
        if not files:
            data['danger'] = 'No photos selected!'
            return render(request, 'website/upload.html', data)

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
        data['success'] = 'Done!'
        return render(request, 'website/upload.html', data)


def contact(request):
    available_languages = Language.objects.all()
    language = get_language_obj(request)

    pagesettings = PageSettings.objects.first()

    data = retrieve_sidemenu_galleries(request, language=language)

    try:
        seo = ContactsPageSeo.objects.get(language=language)
    except ContactsPageSeo.DoesNotExist:
        seo = []

    try:
        contactspage = ContactsPageByLanguage.objects.filter(
            language=language).first()

    except ContactsPageByLanguage.DoesNotExist:
        contactspage = []

    page = ContactsPage.objects.filter()
    if page.exists():
        photos = get_ordered_photos(page.first().photos_order)
    else:
        photos = []
    
    success = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            auto_reply = EmailSend(
                form.cleaned_data['name'],
                form.cleaned_data['message'],
                form.cleaned_data['email'])
            # kitus fieldus kur man sisut nes neprase jis to siust jam mailu
            auto_reply.execute()
            success = 'Sugalvok kaip cia messagas turi atrodyt ir is kur paimamas aka Success'
        else:
            success = False # arba pisk message koki

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
            'success': success,
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
        pricepage = PricePageByLanguage.objects.filter(
            language=language).first()

    except Exception:
        pricepage = []

    try:
        questions = Question.objects.filter(pricepage=pricepage.id)

    except Exception:
        questions = []

    page = PricePage.objects.filter()
    if page.exists():
        photos = get_ordered_photos(page.first().photos_order)
    else:
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
        aboutpage = AboutPageByLanguage.objects.filter(
            language=language).first()

    except Exception:
        aboutpage = []

    page = AboutPage.objects.filter()
    if page.exists():
        photos = get_ordered_photos(page.first().photos_order)
    else:
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

    page = ReviewPage.objects.filter()
    if page.exists():
        photos = get_ordered_photos(page.first().photos_order)
    else:
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
        questions = Question_FaqPage.objects.filter(faqpage=faqpage.id)
    except Exception:
        questions = []
    page = FaqPage.objects.filter()
    if page.exists():
        photos = get_ordered_photos(page.first().photos_order)
    else:
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
    categories = CategoryByLanguage.objects.filter(
        language=language).prefetch_related(
        'category__gallery_set__gallerybylanguage_set').select_related('category')

    data = []

    for category in categories:
        _cat = {'name': category.name}
        _galleries = category.category.gallery_set.all()
        _gals = []           
        for gallery in _galleries:
            _gal = gallery.gallerybylanguage_set.filter(language=language)
            if not _gal.exists():
                continue

            _gal = _gal.first()
            
            _gals.append({'name': _gal.name, 'url': _gal.url})
        _cat.update({'categories': _gals})
        data.append(_cat)
    return data