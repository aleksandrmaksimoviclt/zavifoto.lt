from django.contrib import admin
from .models import *


class AboutPagePhotos(admin.TabularInline):
    model = AboutPagePhoto
    raw_id_fields = ("photo",)


class AboutPageAdmin(admin.ModelAdmin):
    model = AboutPage
    list_display = ('heading', 'language', 'modified',)
    inlines = [AboutPagePhotos,]
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


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        PhotoCategoryAdmin,
        CategoryInline,
    ]


class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        'thumbnail', 'name',
    ]
    exclude = [
        'name',
    ]
    search_fields = [
        'name',
    ]


class GalleryInline(admin.TabularInline):

    model = Photo


#   def get_extra(self, request, obj=None, **kwargs):
#       extra = 2
#       if obj:
#           pass #return extra -
#       return extra


class GalleryByLanguageInline(admin.StackedInline):
    model = GalleryByLanguage


class GalleryAdmin(admin.ModelAdmin):
    inlines = (GalleryByLanguageInline, GalleryInline,)


class QuestionInline(admin.StackedInline):
    model = Question


class PricePageAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class ContactsPageAdmin(admin.ModelAdmin):
    inlines = [
        # ContactsPageByLanguageInline,
    ]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


class PageSettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(PricePage, PricePageAdmin)
admin.site.register(ContactsPage, ContactsPageAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Language)
admin.site.register(PageSettings, PageSettingsAdmin)
admin.site.register(Review)
