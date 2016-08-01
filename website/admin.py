from django.contrib import admin
from .models import *


class PhotoInline(admin.StackedInline):
    model = PhotoCategory


class PhotoAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)


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


class CategoryInline(admin.StackedInline):
    model = CategoryByLanguage

    def get_extra(self, request, obj=None, **kwargs):
        # Kiek rodyti inline childu prie modelio admine
        extra = 2
        if obj:
            pass  # return extra - obj.contactsbylanguage_set.count()
        return extra


class PhotoCategoryAdmin(admin.StackedInline):
    model = PhotoCategory

    def get_extra(self, request, obj=None, **kwargs):
        # Kiek rodyti inline childu prie modelio admine
        extra = 2
        if obj:
            pass  # return extra - obj.contactsbylanguage_set.count()
        return extra


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        PhotoCategoryAdmin,
        CategoryInline,
    ]


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
admin.site.register(AboutPage)
admin.site.register(PricePage, PricePageAdmin)
admin.site.register(ContactsPage, ContactsPageAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Language)
admin.site.register(PageSettings, PageSettingsAdmin)
admin.site.register(Review)
admin.site.register(ComparisonPhoto)