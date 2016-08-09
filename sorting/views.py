
import ast

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from website.models import *
from website.utils import get_ordered_photos


class SortingBaseView(TemplateView):
    template_name = 'sorting/base.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(SortingBaseView, self).dispatch(*args, **kwargs)


class CategoriesSorting(SortingBaseView):
    template_name = 'sorting/categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesSorting, self).get_context_data(**kwargs)
        categories = [{
            'name': cat.__str__(),
            'id': cat.id,
            'url': '/sort/{}/category'.format(cat.id),
            } for cat in Category.objects.all()]
        context.update({'categories': categories})
        return context


class CategorySorting(SortingBaseView):
    template_name = 'sorting/category.html'
    type = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategorySorting, self).get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category_id'])
        category_photos = get_ordered_photos(category.photos_order)
        galleries = [{
            'name': gal.__str__(),
            'id': gal.id,
            'url': '/sort/{}/category/{}/gallery'.format(
                category.id, gal.id)
            } for gal in Gallery.objects.filter(category=category)]
        context.update({
            'galleries': galleries,
            'photos': category_photos,
            'name': category.__str__(),
            'type': self.type,
            'id': category.id})
        return context


class GallerySorting(SortingBaseView):
    template_name = 'sorting/gallery.html'
    type = 'gallery'

    def get_context_data(self, **kwargs):
        context = super(GallerySorting, self).get_context_data(**kwargs)
        gallery = Gallery.objects.get(id=self.kwargs['gallery_id'])
        gallery_photos = get_ordered_photos(gallery.photos_order)
        context.update({
            'name': gallery.__str__,
            'id': gallery.id,
            'photos': gallery_photos,
            'type': self.type})
        return context


class PagesSorting(SortingBaseView):
    template_name = 'sorting/page.html'
    page = None
    type = None

    def get_context_data(self, **kwargs):
        context = super(PagesSorting, self).get_context_data(**kwargs)
        page = self.page.objects.first()
        if page:
            photos = get_ordered_photos(page.photos_order)
            context.update({
                'name': page.__str__,
                'photos': photos,
                'type': self.type})
        return context


class ContactsSorting(PagesSorting):
    page = ContactsPage
    type = 'contacts'


class PricesSorting(PagesSorting):
    page = PricePage
    type = 'price'


class ReviewsSorting(PagesSorting):
    page = Review
    type = 'review'


class AboutSorting(PagesSorting):
    page = AboutPage
    type = 'about'


class FAQSorting(PagesSorting):
    page = FaqPage
    type = 'faq'


TYPES = {
    'category': Category,
    'gallery': Gallery,
    'price': PricePage,
    'review': Review,
    'about': AboutPage,
    'faq': FaqPage,
}


class ChangeOrder(SortingBaseView):

    def post(self, request, *args, **kwargs):
        json = request.read()
        data = ast.literal_eval(json.decode("utf-8"))
        model = TYPES[data['type']]
        qd = {}
        if data['type'] == 'gallery' or data['type'] == 'category':
            qd = {'id': data['id']}
        try:
            obj = model.objects.filter(**qd).first()
            obj.photos_order = data['order']
            obj.save()
            return HttpResponse('Successfully changed order.')
        except Exception as e:
            return HttpResponse(e)
