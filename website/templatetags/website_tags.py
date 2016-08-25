from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy

# reverse_lazy = lambda x: x
register = template.library.Library()


def get_url(url, lang):
    return reverse_lazy(url + '-' + lang)

TRANSLATIONS = {
    'lt': [
        {'url': 'about', 'name': 'Apie mus'},
        {'url': 'reviews','name': 'Atsiliepimai'},
        {'url': 'pricing', 'name': 'Kainos'},
        {'url': 'retouch', 'name': 'Retušavimas'},
        {'url': 'faq', 'name': 'DUK'},
        {'url': 'contacts', 'name': 'Kontaktai'},
        ],
    'en': [
        {'url': 'about', 'name': 'About us'},
        {'url': 'reviews', 'name': 'Reviews'},
        {'url': 'pricing', 'name': 'Prices'},
        {'url': 'retouch', 'name': 'Retouch'},
        {'url': 'faq', 'name': 'FAQ'},
        {'url': 'contacts', 'name': 'Contacts'},           
        ],
    'ru': [
        {'url': 'about', 'name': 'О нас'},
        {'url': 'reviews', 'name': 'Отзывы'},
        {'url': 'pricing', 'name': 'Цены'},
        {'url': 'retouch', 'name': 'Ретуширование'},
        {'url': 'faq', 'name': 'ЧАВО'},
        {'url': 'contacts', 'name': 'Контакты'},
        ]
}


@register.simple_tag
def translated_menu(COOKIES):
    try:
        language = COOKIES['language']
    except KeyError:
        language = 'lt'

    translated = TRANSLATIONS[language]

    menu_html = ''

    for item in translated:
        menu_html += '<li><a href="{}">{}</a></li>'.format(
            get_url(item['url'], language), item['name'])

    return mark_safe(menu_html)


@register.simple_tag
def translate_url(COOKIES, url):
    try:
        language = COOKIES['language']
    except KeyError:
        language = 'lt'

    translated = TRANSLATIONS[language]
    for item in translated:
        if url in item.values():
            return get_url(item['url'], language)
        else:
            return '#'

