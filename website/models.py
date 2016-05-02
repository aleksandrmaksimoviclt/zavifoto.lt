#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.utils.text import slugify




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


class Language(models.Model):
	language_code = models.CharField(max_length=5)
	language = models.CharField(max_length=20)

	def __str__(self):
		return self.language or None


class PageSettings(models.Model):
	style = models.IntegerField(default=0)
	language = models.ForeignKey(Language)
	layout = models.IntegerField(default=0)


class Gallery(models.Model):
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		name = self.galleries_by_languages.all() or None
		return name + ' ' + 'Created'


class GalleryByLanguage(models.Model):
	gallery = models.ForeignKey(Gallery)
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=100, blank=True)
	language = models.ForeignKey(Language)

	def save(self, *args, **kwargs):
		self.url = slugify(self.name)
		super(GalleryByLanguage, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Category(models.Model):
	gallery = models.ForeignKey(Galery)

	def __str__(self):
		return self.gallery


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
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to=image_path)
	gallery = models.ForeignKey(Gallery)
	category = models.ManyToManyField(Category)

	def src(self):
		return self.image.url

	def __str__(self):
		return self.name

	# def save(self, *args, **kwargs):

	# 	return 

# class LandingPage(models.Model):
# 	modified = mdoels.DateTimeField(default=timezone.now)

# 	def __str__(self):
# 		return 'Landing page'


# class LandingPageByLanguage()


class ContactsPage(models.Model):
	address = models.CharField(max_length=100)
	phone = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	# dar prigalvot


class PricePage(models.Model):
	modified = models.DateTimeField(default=timezone.now)


class PricePageByLanguage(models.Model):
	text = models.CharField()
	#  pagalvot
	language = models.ForeignKey(Language)


class Message(models.Model):
	date = models.DateTimeField(default=timezone.now)
	message = models.CharField(max_length=1000)
	contacts = models.CharField(max_length=100)

	