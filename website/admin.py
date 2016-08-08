
from django.contrib import admin
from .models import *


class AboutPagePhotos(admin.TabularInline):
    model = AboutPagePhoto
    raw_id_fields = ("photo",)
    readonly_fields = ('thumbnail',)
    fields = ('photo', 'thumbnail', 'is_side_photo')

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class AboutPageSeo(admin.TabularInline):
    model = AboutPage_Seo
    extra = 1
    max_num = 1


class AboutPageAdmin(admin.ModelAdmin):
    model = AboutPage
    list_display = ('__str__', 'heading', 'language', 'modified',)
    inlines = [AboutPagePhotos, AboutPageSeo]
    fields = (
        'heading', 'quote', 'quote_author', 'text', 'language')

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class CategoryByLanguageSeoInline(admin.TabularInline):
    model = CategoryByLanguage_Seo
    extra = 1
    max_num = 1


class CategoryInline(admin.StackedInline):
    model = CategoryByLanguage

    inlines = [
        CategoryByLanguageSeoInline,
    ]

    def get_extra(self, request, obj=None, **kwargs):
        extra = 3
        if obj:
            return extra - obj.categorybylanguage_set.count()
        return extra


class PhotoCategoryAdmin(admin.TabularInline):
    model = PhotoCategory
    raw_id_fields = ('photo',)
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        return mark_safe(obj.photo.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        PhotoCategoryAdmin,
        CategoryInline,
    ]
    list_display = ('__str__', 'modified')
    exclude = ('photos_order',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        'thumbnail',
        'name',
        'uploaded_at',
    ]
    readonly_fields = ('uploaded_at',)
    search_fields = [
        'name',
    ]


class GalleryInline(admin.TabularInline):
    model = GalleryPhoto
    readonly_fields = ('thumbnail',)
    raw_id_fields = ('photo',)

    def thumbnail(self, obj):
        return mark_safe(obj.photo.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class GalleryByLanguageInline(admin.TabularInline):
    model = GalleryByLanguage


class GalleryAdmin(admin.ModelAdmin):
    inlines = (
        GalleryByLanguageInline,
        GalleryInline,)

    exclude = ('photos_order', 'created')
    list_display = ('__str__', 'modified',)


class FaqPhotosInline(admin.TabularInline):
    model = FAQPhoto
    raw_id_fields = ("photo",)
    readonly_fields = ('thumbnail',)
    fields = ('photo', 'thumbnail', 'is_side_photo')

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class QuestionFAQInline(admin.StackedInline):
    model = Question_FaqPage
    extra = 1


class FaqPageSeoInline(admin.TabularInline):
    model = FaqPage_Seo
    extra = 1
    max_num = 1


class FaqPageAdmin(admin.ModelAdmin):
    inlines = [QuestionFAQInline, FaqPhotosInline, FaqPageSeoInline]
    exclude = ('modified',)
    list_display = ('__str__', 'language', 'modified')


class QuestionInline(admin.StackedInline):
    model = Question


class PricePhotosInline(admin.TabularInline):
    model = PricePagePhoto
    raw_id_fields = ("photo",)
    readonly_fields = ('thumbnail',)
    fields = ('photo', 'thumbnail', 'is_side_photo')

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class PricePageSeoInline(admin.TabularInline):
    model = PricePage_Seo
    extra = 1
    max_num = 1


class PricePageAdmin(admin.ModelAdmin):
    inlines = [PricePhotosInline, QuestionInline, PricePageSeoInline]
    list_display = ('__str__', 'heading', 'language', 'modified',)


class ContactsPhotosInline(admin.TabularInline):
    model = ContactsPagePhoto
    raw_id_fields = ("photo",)
    readonly_fields = ('thumbnail',)
    fields = ('photo', 'thumbnail', 'is_side_photo')

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class ContactsPageSeoInline(admin.TabularInline):
    model = ContactsPage_Seo
    extra = 1
    max_num = 1


class ContactsPageAdmin(admin.ModelAdmin):
    inlines = [
        ContactsPhotosInline,
        ContactsPageSeoInline
    ]
    list_display = ('__str__', 'language')

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class PageSettingsAdmin(admin.ModelAdmin):
    list_display = ('style', 'language', 'layout')

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


class ReviewAdminInline(admin.TabularInline):
    model = ReviewPhoto
    raw_id_fields = ('photo',)
    fields = ('photo', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        return mark_safe(obj.photo.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    inlines = (ReviewAdminInline,)
    fields = ('author', 'review',)
    list_display = ('__str__', 'author', 'created_at')
    exclude = ('created_at',)


class ComparisonPhotoAdmin(admin.ModelAdmin):
    model = ComparisonPhoto

    list_display = ('before_thumb', 'after_thumb')

    def before_thumb(self, obj):
        return mark_safe(
            '<img src="{}" width=60 height=60>'.format(obj.before.url))
    before_thumb.short_description = u"Before"

    def after_thumb(self, obj):
        return mark_safe(
            '<img src="{}" width=60 height=60>'.format(obj.before.url))
    after_thumb.short_description = u"After"


class IndexPageInline(admin.TabularInline):
    model = IndexPage_Seo
    extra = 1
    max_num = 1


class IndexPageAdmin(admin.ModelAdmin):
    model = IndexPage
    inlines = [IndexPageInline]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class RetouchPageInline(admin.TabularInline):
    model = RetouchPage_Seo
    extra = 1
    max_num = 1


class RetouchPageAdmin(admin.ModelAdmin):
    model = RetouchPage
    inlines = [RetouchPageInline]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Category, CategoryAdmin)
# no seo on top ------------------
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(FaqPage, FaqPageAdmin)
admin.site.register(PricePage, PricePageAdmin)
admin.site.register(ContactsPage, ContactsPageAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Language)
admin.site.register(PageSettings, PageSettingsAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ComparisonPhoto, ComparisonPhotoAdmin)
admin.site.register(IndexPage, IndexPageAdmin)
admin.site.register(RetouchPage, RetouchPageAdmin)
