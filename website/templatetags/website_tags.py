# from django import template
# from django.core.urlresolvers import reverse
# from django.utils.safestring import mark_safe
# from website.models import *

# @register.simple_tag
# def get_category_name(project_id, language):
# 	try:
# 		return ProjectByLanguage.objects.get(project__id=project_id, language__language_code=language).slug
# 	except Exception as e:
# 		logger.error(e)
# 		return ''

# def get_category_slug(project_id, language):
# 	try:
# 		return ProjectByLanguage.objects.get(project__id=project_id, language__language_code=language).slug
# 	except Exception as e:
# 		logger.error(e)
# 		return ''