	## TODO - 
##		READ ABOUT INLINES
## 		TABULARINLINE <-
## 		DJANGO ADMIN
##		to hide model field - EXCLUDE command
##		unique 

from django.contrib import admin
from .models import * 


# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
	list_display = [
	'thumbnail', 'name', 
	]
	exclude = [ 'name',
	]
	search_fields = [ 'name',
	]

class GalleryInline(admin.TabularInline):

	model = Photo


	def get_extra(self, request, obj=None, **kwargs):
	    extra = 2
	    if obj:
	        pass #return extra - 
	    return extra


class GalleryByLanguageInline(admin.StackedInline):
	model = GalleryByLanguage



class GalleryAdmin(admin.ModelAdmin):
	inlines = [
		GalleryByLanguageInline,
		GalleryInline,
	]
	# def photos(self):
	# 	return 'test'#Photo.objects.all()
	# photos.allow_html = True
	# fields = [photos,]

class CategoryInline(admin.StackedInline):
	model = CategoryByLanguage

	def get_extra(self, request, obj=None, **kwargs):
		## Kiek rodyti inline childu prie modelio admine
	    extra = 2
	    if obj:
	        pass #return extra - obj.contactsbylanguage_set.count()
	    return extra


class CategoryAdmin(admin.ModelAdmin):
	inlines = [
		CategoryInline,
	]


class AboutPagePhotoInline(admin.TabularInline):
	model = AboutPagePhoto
	extra = 1

	def __str__(self):
		return 'About page photo'

class AboutPageByLanguageInline(admin.StackedInline):
	model = AboutPageByLanguage

	def get_extra(self, request, obj=None, **kwargs):
	    extra = 2
	    if obj:
	        pass #return extra - obj.contactsbylanguage_set.count()
	    return extra


class AboutPageAdmin(admin.ModelAdmin):
	inlines = [
		AboutPageByLanguageInline,
		AboutPagePhotoInline
	]

	def has_add_permission(self, request):
		return False if self.model.objects.count() > 0 else True


class PricePageByLanguageInline(admin.StackedInline):
	model = PricePageByLanguage

	def get_extra(self, request, obj=None, **kwargs):
	    extra = 2
	    if obj:
	        pass #return extra - obj.contactsbylanguage_set.count()
	    return extra


class PricePageAdmin(admin.ModelAdmin):
	inlines = [
		PricePageByLanguageInline,
	]

	def has_add_permission(self, request):
		return False if self.model.objects.count() > 0 else True


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