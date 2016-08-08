from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.SortingBaseView.as_view(), name='photosorting'),
    url(r'^change-order$', views.ChangeOrder.as_view(), name='change-order'),
    url(r'^categories$', views.CategoriesSorting.as_view()),
    url(r'^contacts$', views.ContactsSorting.as_view()),
    url(r'^prices$', views.PricesSorting.as_view()),
    url(r'^reviews$', views.ReviewsSorting.as_view()),
    url(r'^about$', views.AboutSorting.as_view()),
    url(r'^faq$', views.FAQSorting.as_view()),
    url(r'^(?P<category_id>\w+)/category$', views.CategorySorting.as_view()),
    url(
        r'^(?P<category_id>\w+)/category/(?P<gallery_id>\w+)/gallery$',
        views.GallerySorting.as_view()),
]
