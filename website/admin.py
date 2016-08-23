
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


class AboutPageSeoInline(admin.TabularInline):
    model = AboutPageSeo
    extra = 3
    max_num = 3


class AboutPageByLanguageInline(admin.TabularInline):
    model = AboutPageByLanguage
    extra = 3
    max_num = 3


class AboutPageAdmin(admin.ModelAdmin):
    model = AboutPage
    readonly_fields = ('modified',)
    exclude = ('photos_order',)
    inlines = [AboutPagePhotos, AboutPageSeoInline, AboutPageByLanguageInline]
    list_display = ('__str__',)

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class CategoryByLanguageSeoInline(admin.TabularInline):
    model = CategorySeo
    extra = 3
    max_num = 3


class CategoryInline(admin.StackedInline):
    model = CategoryByLanguage

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
    model = FaqPageSeo
    extra = 1
    max_num = 1


class FaqPageAdmin(admin.ModelAdmin):
    inlines = [QuestionFAQInline, FaqPhotosInline, FaqPageSeoInline]
    exclude = ('photos_order',)
    readonly_fields = ('modified',)
    list_display = ('__str__', 'modified')


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
    model = PricePageSeo
    extra = 1
    max_num = 1


class PricePageByLanguageInline(admin.TabularInline):
    model = PricePageByLanguage


class PricePageAdmin(admin.ModelAdmin):
    inlines = [PricePhotosInline, QuestionInline, PricePageSeoInline, PricePageByLanguageInline]
    exclude = ('photos_order',)
    list_display = ('__str__',)


class ContactsPhotosInline(admin.TabularInline):
    model = ContactsPagePhoto
    raw_id_fields = ("photo",)
    readonly_fields = ('thumbnail',)
    fields = ('photo', 'thumbnail', 'is_side_photo')

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class ContactsPageSeoInline(admin.TabularInline):
    model = ContactsPageSeo
    extra = 3
    max_num = 3


class ContactsPageByLanguageInline(admin.TabularInline):
    model = ContactsPageByLanguage


class ContactsPageAdmin(admin.ModelAdmin):
    inlines = [
        ContactsPhotosInline,
        ContactsPageSeoInline,
        ContactsPageByLanguageInline,
    ]
    exclude = ('photos_order',)
    list_display = ('__str__',)

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class PageSettingsAdmin(admin.ModelAdmin):
    list_display = ('style', 'language', 'layout')

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


class ReviewByLanguageInline(admin.TabularInline):
    model = ReviewByLanguage


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    inlines = (ReviewByLanguageInline,)
    raw_id_fields = ('photo',)
    fields = ('photo', 'thumbnail')
    readonly_fields = ('thumbnail',)
    list_display = ('__str__', 'created_at',)

    def thumbnail(self, obj):
        return mark_safe(obj.photo.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class ReviewPagePhotosInline(admin.TabularInline):
    model = ReviewPagePhoto
    raw_id_fields = ("photo",)
    readonly_fields = ('thumbnail',)
    fields = ('photo', 'thumbnail', 'is_side_photo')

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class ReviewPageByLanguageInline(admin.TabularInline):
    model = ReviewPageByLanguage
    max_num = 3


class ReviewPageAdmin(admin.ModelAdmin):
    model = ReviewPage
    inlines = (ReviewPageByLanguageInline,ReviewPagePhotosInline,)
    list_display = ('__str__',)
    exclude =('photos_order',)


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
    model = IndexPageSeo
    extra = 3
    max_num = 3


class IndexPhotosInline(admin.TabularInline):
    model = IndexPagePhoto
    raw_id_fields = ('photo',)
    fields = ('photo', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        return mark_safe(obj.photo.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class IndexPageAdmin(admin.ModelAdmin):
    model = IndexPage
    exclude = ('photos_order',)
    inlines = [IndexPageInline, IndexPhotosInline]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class RetouchPageInline(admin.TabularInline):
    model = RetouchPageSeo
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
admin.site.register(ReviewPage, ReviewPageAdmin)
