#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from collections import OrderedDict

from django.db import models
from django.utils import timezone
from django.utils.text import slugify, mark_safe
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from redactor.fields import RedactorField


WHITE = 0
BLACK = 1

DEFAULT_LANGUAGE = 'lt'

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


def delete_from_order(obj, id):
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


def get_order_num(order):
    try:
        return str(int(max(order.keys())) + 1)
    except (AttributeError, ValueError):
        return str(1)

class Cms(models.Model):
    top_text = models.TextField(blank=True, null=True)
    main_text = models.TextField(blank=True, null=True)
    bottom_text = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Language(models.Model):
    language_code = models.CharField(max_length=5)
    language = models.CharField(max_length=20)
    # is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.language or None

class VerificationCode(models.Model):
    google_site_verification = models.CharField(max_length=1000)
    google_analytics_verification = models.CharField(max_length=1000)


class PageSettings(models.Model):
    style = models.IntegerField(choices=STYLES, default=WHITE)
    language = models.ForeignKey(Language)
    layout = models.IntegerField(choices=LAYOUTS, default=GRID)

    class Meta:
        verbose_name_plural = 'Default Settings'
        verbose_name = verbose_name_plural

    def __str__(self):
        return 'Default Settings'

class Gallery(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    photos_order = JSONField(default={}, blank=True, null=True)
    category = models.ForeignKey('Category', null=True)

    class Meta(object):
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return self.name

    @property
    def name(self):
        try:
            return self.gallerybylanguage_set.all().get(
                language__language='lt').name
        except IndexError:
            return 'Untitled gallery '
        except Exception:
            return 'Untitled gallery '

    def remove_from_order(self, id):
        delete_from_order(self, id)


class GalleryByLanguage(models.Model):
    gallery = models.ForeignKey(Gallery)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)
    language = models.ForeignKey(Language)

    class Meta(object):
        unique_together = (('gallery', 'language'),)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.name)
        super(GalleryByLanguage, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class GalleryByLanguage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    gallerybylanguage = models.ForeignKey(GalleryByLanguage, null=True)

class Category(models.Model):

    photos_order = JSONField(default={}, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        _categories = self.categorybylanguage_set
        if _categories.exists():
            return _categories.first().name
        else:
            return 'Category by language is not attached'

    def remove_from_order(self, id):
        delete_from_order(self, id)

    def __str__(self):
        try:
            return self.categorybylanguage_set.filter(
                language__language_code='lt').first().name
        except IndexError:
            return 'Untitled gallery '
        except Exception:
            return 'Untitled gallery '


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

class CategoryByLanguage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    categorybylanguage = models.ForeignKey(CategoryByLanguage ,null=True)


def image_path(instance, filename):
    return '/'.join([str(instance) + '_' + filename])


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=image_path)
    gallery = models.ForeignKey(Gallery, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    @property
    def src(self):
        return self.image.url

    @property
    def thumbnail(self):
        return mark_safe('<img src="%s" width=60 height=60>' % self.image.url)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            order_num = get_order_num(self.gallery.photos_order)
            self.gallery.photos_order[order_num] = str(self.id)
            self.gallery.save()
        if not self.name:
            self.name = self.image.name
        super(Photo, self).save(*args, **kwargs)


@receiver(
    pre_delete, sender=Photo,
    dispatch_uid='photos_delete_from_order_signal')
def delete_photos_from_order(sender, instance, using, **kwargs):
    try:
        instance.gallery.remove_from_order(instance.id)
    except Gallery.DoesNotExist:
        pass


class PhotoCategory(models.Model):
    photo = models.ForeignKey(Photo, related_name='photos')
    category = models.ForeignKey(Category)

    class Meta:
        unique_together = (('photo', 'category'),)
        verbose_name = 'Photo for category'
        verbose_name_plural = 'Photos for category'

    def save(self, *args, **kwargs):
        order_num = get_order_num(self.category.photos_order)
        self.category.photos_order[order_num] = str(self.photo.id)
        self.category.save()
        super(PhotoCategory, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.category.remove_from_order(self.id)
        super(PhotoCategory, self).delete(*args, **kwargs)


@receiver(
    pre_delete, sender=PhotoCategory,
    dispatch_uid='photos_delete_from_category_order_signal')
def delete_photos_from_category_order(sender, instance, using, **kwargs):
    instance.category.remove_from_order(instance.photo.id)


class AbstractPage(models.Model):
    heading = RedactorField()
    heading_slug = RedactorField()
    message = RedactorField()
    e_mail = RedactorField()
    phone_number = RedactorField()
    top_text = RedactorField()
    photo = RedactorField()
    author = RedactorField()
    text_with_icons_on_left = RedactorField()

    class Meta:
        abstract = True


class ContactsPage(models.Model):
    page_name_in_menu = models.CharField(max_length=100)
    photos_order = JSONField(default={}, null=True, blank=True)
    page_title = models.CharField(max_length=100)
    heading = RedactorField(verbose_name=u'Heading')
    heading_text = RedactorField(verbose_name=u'Heading Text')
    email = models.CharField(max_length=254, blank=True, null=True)
    phone_number_display = models.CharField(
        max_length=20, blank=True, null=True)
    phone_number_call = models.CharField(max_length=20, blank=True, null=True)
    contact_form_heading = models.CharField(
        max_length=50, blank=True, null=True)
    contact_form_name = models.CharField(max_length=50, blank=True, null=True)
    contact_form_email = models.CharField(max_length=50, blank=True, null=True)
    contact_form_phone_number = models.CharField(
        max_length=50, blank=True, null=True)
    contact_form_question = models.CharField(
        max_length=50, blank=True, null=True)
    contact_form_message = models.CharField(
        max_length=50, blank=True, null=True)
    contact_form_send_button_text = models.CharField(
        max_length=50, blank=True, null=True)
    language = models.ForeignKey(Language, null=True)

    class Meta:
        verbose_name_plural = 'Contacts Page'

    def description(self):
        if self.description_editor or self.adasd or self.sodasdasd:
            return mark_safe(self.description_editor)

    def __str__(self):
        return 'Kontaktai ' + self.language.language_code + ' kalba'

class ContactsPage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    contactspage = models.ForeignKey(ContactsPage ,null=True)


class ContactsPagePhoto(models.Model):
    contacts_page = models.ForeignKey(ContactsPage, related_name='photos')
    photo = models.ForeignKey(Photo, unique=True)
    is_side_photo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            order_num = get_order_num(self.review.photos_order)
            self.review.photos_order[order_num] = str(self.photo.id)
            self.review.save()
        super(ReviewPhoto, self).save(*args, **kwargs)


@receiver(
    pre_delete, sender=ContactsPagePhoto,
    dispatch_uid='photos_delete_from_contacts_order_signal')
def delete_photos_from_contacts_order(sender, instance, using, **kwargs):
    delete_from_order(instance.contacts_page, instance.photo.id)


class PricePage(models.Model):
    page_name_in_menu = models.CharField(max_length=100)
    photos_order = JSONField(default={}, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    heading = models.CharField(max_length=100, null=True, blank=True)
    language = models.ForeignKey(Language, null=True)

    def __str__(self):
        return 'Pricepage ' + self.language.language_code

    class Meta:
        verbose_name_plural = 'Price Page'

class PricePage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    pricepage = models.ForeignKey(PricePage ,null=True)

class PricePagePhoto(models.Model):
    price_page = models.ForeignKey(PricePage, related_name='photos')
    photo = models.ForeignKey(Photo, unique=True)
    is_side_photo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            order_num = get_order_num(self.price_page.photos_order)
            self.price_page.photos_order[order_num] = str(self.photo.id)
            self.price_page.save()
        super(PricePagePhoto, self).save(*args, **kwargs)


@receiver(
    pre_delete, sender=PricePagePhoto,
    dispatch_uid='photos_delete_from_prices_order_signal')
def delete_photos_from_prices_order(sender, instance, using, **kwargs):
    delete_from_order(instance.price_page, instance.photo.id)


class Question(models.Model):
    heading = models.CharField(max_length=100, null=True, blank=True)
    body = RedactorField(verbose_name=u'Question Body', null=True, blank=True)
    pricepage = models.ForeignKey(PricePage, on_delete=models.CASCADE)


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
    page_name_in_menu = models.CharField(max_length=100)
    photos_order = JSONField(default={}, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now)
    heading = models.CharField(max_length=100, null=True, blank=True)
    quote = RedactorField(verbose_name=u'Quote', null=True, blank=True)
    quote_author = RedactorField(
        verbose_name=u'Quote author', null=True, blank=True)
    text = RedactorField(verbose_name=u'Text', null=True, blank=True)

    language = models.ForeignKey(Language, null=True, unique=True)

    class Meta:
        verbose_name_plural = 'About Page'

    def __str__(self):
        return 'About page ' + self.language.language_code

class AboutPage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    aboutpage = models.ForeignKey(AboutPage ,null=True)

class AboutPagePhoto(models.Model):
    about = models.ForeignKey('AboutPage', related_name='photos')
    photo = models.ForeignKey(Photo, unique=True)
    is_side_photo = models.BooleanField(default=False)

    def __str__(self):
        return 'About page photo'

    def save(self, *args, **kwargs):
        if self._state.adding:
            order_num = get_order_num(self.about.photos_order)
            self.about.photos_order[order_num] = str(self.photo.id)
            self.about.save()
        super(AboutPagePhoto, self).save(*args, **kwargs)


@receiver(
    pre_delete, sender=AboutPagePhoto,
    dispatch_uid='photos_delete_from_about_order_signal')
def delete_photos_from_about_order(sender, instance, using, **kwargs):
    delete_from_order(instance.about, instance.photo.id)


class Review(models.Model):
    photos_order = JSONField(default={}, null=True, blank=True)
    review = RedactorField(verbose_name=u'Review')
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def text(self):
        if self.review:
            return mark_safe(self.review)

    def __str__(self):
        return self.author


class ReviewPhoto(models.Model):
    review = models.ForeignKey('Review', related_name='photos')
    photo = models.ForeignKey('Photo')
    is_side_photo = models.BooleanField(default=False)

class ReviewPage(models.Model):
    language = models.ForeignKey(Language, null=True)

class ReviewPage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    reviewpage = models.ForeignKey(ReviewPage, null=True)


class FaqPage(models.Model):
    page_name_in_menu = models.CharField(max_length=100)
    photos_order = JSONField(default={}, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now)
    heading = models.CharField(max_length=100, null=True, blank=True)
    language = models.ForeignKey(Language, null=True)

    class Meta:
        verbose_name_plural = 'FAQ Page'

    def __str__(self):
        return 'FAQ Page ' + self.language.language_code
    def save(self, *args, **kwargs):
        if self._state.adding:
            order_num = get_order_num(self.review.photos_order)
            self.review.photos_order[order_num] = str(self.photo.id)
            self.review.save()
        super(ReviewPhoto, self).save(*args, **kwargs)


@receiver(
    pre_delete, sender=ReviewPhoto,
    dispatch_uid='photos_delete_from_review_order_signal')
def delete_photos_from_review_order(sender, instance, using, **kwargs):
    delete_from_order(instance.review, instance.photo.id)

class FaqPage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    faqpage = models.ForeignKey(FaqPage ,null=True)


class Question_FaqPage(models.Model):
    heading = models.CharField(max_length=100, null=True, blank=True)
    body = RedactorField(verbose_name=u'Question Body', null=True, blank=True)
    faqpage = models.ForeignKey(FaqPage, on_delete=models.CASCADE)


class FAQPhoto(models.Model):
    faq_page = models.ForeignKey(FaqPage, related_name='photos')
    photo = models.ForeignKey(Photo, unique=True)
    is_side_photo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            order_num = get_order_num(self.faq_page.photos_order)
            self.faq_page.photos_order[order_num] = str(self.photo.id)
            self.faq_page.save()
        super(FAQPhoto, self).save(*args, **kwargs)

@receiver(
    pre_delete, sender=FAQPhoto,
    dispatch_uid='photos_delete_from_faq_order_signal')
def delete_photos_from_faq_order(sender, instance, using, **kwargs):
    delete_from_order(instance.faq_page, instance.photo.id)

class RetouchPage(models.Model):
    page_name_in_menu = models.CharField(max_length=100)
    language = models.ForeignKey(Language, null=True)

class RetouchPage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    retouchpage = models.ForeignKey(RetouchPage,null=True)

class ComparisonPhoto(models.Model):
    before = models.ImageField(upload_to='retouch/')
    after = models.ImageField(upload_to='retouch/')
    name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

class IndexPage(models.Model):
    language = models.ForeignKey(Language, null=True)

class IndexPage_Seo(models.Model):
    page_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=156)
    title_for_facebook = models.CharField(max_length=27)
    description_for_facebook = models.CharField(max_length=300)
    image_for_facebook = models.ImageField(upload_to='seo/')
    indexpage = models.ForeignKey(IndexPage,null=True)