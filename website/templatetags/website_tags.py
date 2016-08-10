from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy

# reverse_lazy = lambda x: x
register = template.library.Library()

@register.simple_tag
def translated_menu(COOKIES):
    translations = {
        'lt': [
            {'url': reverse_lazy('contacts-lt'), 'name': 'Kontaktai'},
            {'url': reverse_lazy('retouch-lt'), 'name': 'Retušavimas'},
            {'url': reverse_lazy('pricing-lt'), 'name': 'Kainos'},
            {'url': reverse_lazy('about-lt'), 'name': 'Apie mus'},
            {'url': reverse_lazy('reviews-lt'),'name': 'Atsiliepimai'},
            {'url': reverse_lazy('faq-lt'), 'name': 'DUK'}],
        'en': [
            {'url': reverse_lazy('contacts-en'), 'name': 'Contacts'},
            {'url': reverse_lazy('retouch-en'), 'name': 'Retouch'},
            {'url': reverse_lazy('pricing-en'), 'name': 'Prices'},
            {'url': reverse_lazy('about-en'), 'name': 'About us'},
            {'url': reverse_lazy('reviews-en'),'name': 'Reviews'},
            {'url': reverse_lazy('faq-en'), 'name': 'FAQ'}],
        'ru': [
            {'url': reverse_lazy('contacts-ru'), 'name': 'Контакты'},
            {'url': reverse_lazy('retouch-ru'), 'name': 'Ретуширование'},
            {'url': reverse_lazy('pricing-ru'), 'name': 'Цены'},
            {'url': reverse_lazy('about-ru'), 'name': 'О нас'},
            {'url': reverse_lazy('reviews-ru'),'name': 'Отзывы'},
            {'url': reverse_lazy('faq-ru'), 'name': 'ЧАВО'}]
    }
    
    try:
        language = COOKIES['language']
    except KeyError:
        language = 'lt'

    translated = translations[language]

    menu_html = ''

    for item in translated:
        menu_html += '<li><a href="{}">{}</a></li>'.format(item['url'], item['name'])

    return mark_safe(menu_html)