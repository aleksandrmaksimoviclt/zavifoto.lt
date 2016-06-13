#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField
from collections import OrderedDict
import uuid



WHITE = 0
BLACK = 1


STYLES = (
	(WHITE, 'White page style'),
	(BLACK, 'Black page style'),
)


GRID = 0
SLIDE = 1

LAYOUTS = (
	(GRID, 'Grid landing'),
	(SLIDE, 'Full screen sliding'),
)

def get_order_num(order):
	try:
		return str(int(max(order.keys())) + 1)
	except ValueError:
		return str(1)


def sorted_order(photos_order):
	ordered = OrderedDict()
	for photo in sorted(photos_order.keys()):
		ordered.update({photo: photos_order[photo]})
	photos = OrderedDict()
	for key, value in ordered.items():
		try:
			photos.update({key: Photo.objects.get(id=value)})
		except ValueError:
			pass
	return photos

def delete_photo_from_order(obj, id):
	popped_key = None
	new_order = OrderedDict()
	for key, value in obj.photos_order.items():
		if popped_key:
			new_key = str(int(key) - 1)
			new_order.update({new_key: value})
		
		elif value == id:
			popped_key = key
			obj.photos_order.pop(key)

	obj.photos_order = new_order
	obj.save()


class Language(models.Model):
	language_code = models.CharField(max_length=5)
	language = models.CharField(max_length=20)

	def __str__(self):
		return self.language or None


class PageSettings(models.Model):
	style = models.IntegerField(choices=STYLES, default=WHITE)
	language = models.ForeignKey(Language)
	layout = models.IntegerField(choices=LAYOUTS, default=GRID)

	class Meta:
		verbose_name_plural = 'Page Default Settings'
		verbose_name = verbose_name_plural


class Gallery(models.Model):
	created = models.DateTimeField(default=timezone.now)
	category = models.ForeignKey('Category', null=True)
	photos_order = JSONField(default={}, blank=True, null=True)
	
	class Meta:
		verbose_name_plural = 'Galleries'

	def __str__(self):
		return self.name
	
	@property	
	def name(self):
		try:
			return self.gallerybylanguage_set.all()[0].name
		except IndexError:
			return 'Untitled gallery '
		except Exception:
			return 'Untitled gallery '
	
	def get_photos_by_order(self):
		return sorted_order(self.photos_order)

	def remove_from_order(self, id):
		delete_photo_from_order(self, id)


class GalleryByLanguage(models.Model):
	gallery = models.ForeignKey(Gallery)
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=100, blank=True)
	language = models.ForeignKey(Language)

	class Meta:
		unique_together = (('gallery', 'language'),)

	def save(self, *args, **kwargs):
		if not self.url:
			self.url = slugify(self.name)
		super(GalleryByLanguage, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Category(models.Model):
	photos_order = JSONField(default={}, null=True, blank=True)
	# 'page settings for categories'

	class Meta:
		verbose_name_plural = 'Categories'

	def get_photos_by_order(self):
		return sorted_order(self.photos_order)

	def remove_from_order(self, id):
		delete_photo_from_order(self, id)


class CategoryByLanguage(models.Model):
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=100)
	language = models.ForeignKey(Language)
	url = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.url = slugify(self.name)
		super(CategoryByLanguage, self).save(*args, **kwargs)


def image_path(instance, filename):
    return '/'.join([str(instance) + '_' + filename])

class Photo(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100, blank=True, null=True)
	image = models.ImageField(upload_to=image_path)
	gallery = models.ForeignKey(Gallery)

	def src(self):
		return self.image.url

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		order_num = get_order_num(self.gallery.photos_order)
		self.gallery.photos_order[order_num] = str(self.id)
		self.gallery.save()
		if not self.name:
			self.name = self.image.name
		super(Photo, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.gallery.remove_from_order(self.id)
		super(Photo, self).delete(*args, **kwargs)


class PhotoCategory(models.Model):
	photo = models.ForeignKey(Photo)
	category = models.ForeignKey(Category)

	class Meta:
		unique_together = (('photo', 'category'),)

	def save(self, *args, **kwargs):
		order_num = get_order_num(self.category.photos_order)
		self.category.photos_order[order_num] = str(self.photo.id)
		self.category.save()
		super(PhotoCategory, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.category.remove_from_order(self.id)
		super(PhotoCategory, self).delete(*args, **kwargs)


class AbstractPage(models.Model):
	top_text = models.TextField(blank=True, null=True)
	main_text = models.TextField(blank=True, null=True)
	bottom_text = models.TextField(blank=True, null=True)
	
	class Meta:
		abstract = True

class ContactsPage(AbstractPage):
	address = models.CharField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(max_length=50, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Contacts Page'

	def __str__(self):
		return 'Contacts Page'

class ContactsPagePhoto(models.Model):
	contacts_page = models.ForeignKey(ContactsPage)
	photo = models.ForeignKey(Photo, unique=True)


class PricePage(models.Model):
	modified = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return 'Prices page settings'

	class Meta:
		verbose_name_plural = 'Price Page'

class PricePagePhoto(models.Model):
	price_page = models.ForeignKey(PricePage)
	photo = models.ForeignKey(Photo, unique=True)


class PricePageByLanguage(AbstractPage):
	pricepage = models.ForeignKey(PricePage)
	language = models.ForeignKey(Language)

	def __str__(self):
		return self.language.language_code or None


class Message(models.Model):
	date = models.DateTimeField(default=timezone.now)
	message = models.CharField(max_length=1000)
	sender = models.CharField(max_length=100)
	read = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		super(Message, self).save(*args, **kwargs)

	def __str__(self):
		status = ''
		if not self.read:
			status = '(Unread)'
		return '{0} message{1}'.format(self.sender, status)


class AboutPage(models.Model):
	modified = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name_plural = 'About Page'

	def __str__(self):
		return 'About Page'


class AboutPagePhoto(models.Model):
	about = models.ForeignKey(AboutPage)
	photo = models.ForeignKey(Photo, unique=True)

	def __str__(self):
		return 'About page photo'

	def tumbnail(self):
		pass


class AboutPageByLanguage(AbstractPage):
	language = models.ForeignKey(Language)
	about_page = models.ForeignKey(AboutPage)
	
	def __str__(self):
		return self.language.language_code + 'about page' or None

class FAQPage(models.Model):
	modified = models.DateTimeField(default=timezone.now)


class FAQPhoto(models.Model):
	faq_page = models.ForeignKey(FAQPage)
	photo = models.ForeignKey(Photo, unique=True)


class FAQPageByLanguage(AbstractPage):
	language = models.ForeignKey(Language, unique=True)

class FAQQuestion(models.Model):
	faq_page_by_language = models.ForeignKey(FAQPageByLanguage)
	title = models.TextField()
	text = models.TextField()
