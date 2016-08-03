from django.contrib import admin
from .models import *


class AboutPagePhotos(admin.TabularInline):
    model = AboutPagePhoto
    raw_id_fields = ("photo",)


class AboutPageAdmin(admin.ModelAdmin):
    model = AboutPage
    list_display = ('__str__', 'heading', 'language', 'modified',)
    inlines = [AboutPagePhotos]
    fields = (
        'heading', 'quote', 'quote_author', 'text', 'language')


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
    model = Photo
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        return mark_safe(obj.thumbnail)
    thumbnail.short_description = u"Thumbnail"


class GalleryByLanguageInline(admin.TabularInline):
    model = GalleryByLanguage


class GalleryAdmin(admin.ModelAdmin):
    inlines = (
        GalleryByLanguageInline,
        GalleryInline,)

    exclude = ('photos_order', 'created')
    list_display = ('__str__', 'modified',)


class Question_FAQInline(admin.StackedInline):
    model = Question_FaqPage


class FaqPageAdmin(admin.ModelAdmin):
    inlines = [Question_FAQInline]


class QuestionInline(admin.StackedInline):
    model = Question


class PricePageAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('__str__', 'heading', 'language', 'modified',)


class ContactsPageAdmin(admin.ModelAdmin):
    inlines = [
        # ContactsPageByLanguageInline,
    ]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True


class PageSettingsAdmin(admin.ModelAdmin):
    list_display = ('style', 'language', 'layout')

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    raw_id_fields = ('photo',)
    fields = ('author', 'review', 'photo', 'thumbnail')
    readonly_fields = ('thumbnail',)
    list_display = ('__str__', 'author', 'thumbnail', 'created_at')
    exclude = ('created_at',)

    def thumbnail(self, obj):
        return mark_safe(obj.photo.thumbnail)
    thumbnail.short_description = u"Thumbnail"


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(FaqPage, FaqPageAdmin)
admin.site.register(PricePage, PricePageAdmin)
admin.site.register(ContactsPage, ContactsPageAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Language)
admin.site.register(PageSettings, PageSettingsAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ComparisonPhoto)
