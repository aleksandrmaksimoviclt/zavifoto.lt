from django.db import models

from redactor.fields import RedactorField


class EmailAutoReplySettings(models.Model):
	subject = models.CharField(max_length=100)
	text = RedactorField(verbose_name=u'Auto Reply text')