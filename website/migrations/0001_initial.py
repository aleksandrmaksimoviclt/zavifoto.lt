# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-05 07:03
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import redactor.fields
import uuid
import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('heading', models.CharField(blank=True, max_length=100, null=True)),
                ('quote', redactor.fields.RedactorField(blank=True, null=True, verbose_name='Quote')),
                ('quote_author', redactor.fields.RedactorField(blank=True, null=True, verbose_name='Quote author')),
                ('text', redactor.fields.RedactorField(blank=True, null=True, verbose_name='Text')),
            ],
            options={
                'verbose_name_plural': 'About Page',
            },
        ),
        migrations.CreateModel(
            name='AboutPagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_side_photo', models.BooleanField(default=False)),
                ('about', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.AboutPage')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos_order', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryByLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ComparisonPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('before', models.ImageField(upload_to='retouch/')),
                ('after', models.ImageField(upload_to='retouch/')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactsPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_title', models.CharField(max_length=100)),
                ('heading', redactor.fields.RedactorField(verbose_name='Heading')),
                ('heading_text', redactor.fields.RedactorField(verbose_name='Heading Text')),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('phone_number_display', models.CharField(blank=True, max_length=20, null=True)),
                ('phone_number_call', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_form_heading', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_form_name', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_form_email', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_form_phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_form_question', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_form_message', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_form_send_button_text', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Contacts Page',
            },
        ),
        migrations.CreateModel(
            name='ContactsPagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_side_photo', models.BooleanField(default=False)),
                ('contacts_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.ContactsPage')),
            ],
        ),
        migrations.CreateModel(
            name='FaqPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('heading', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'FAQ Page',
            },
        ),
        migrations.CreateModel(
            name='FAQPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_side_photo', models.BooleanField(default=False)),
                ('faq_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.FaqPage')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('photos_order', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Category')),
            ],
            options={
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='GalleryByLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=100)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=5)),
                ('language', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.CharField(max_length=1000)),
                ('sender', models.CharField(max_length=100)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PageSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.IntegerField(choices=[(0, 'White page style'), (1, 'Black page style')], default=0)),
                ('layout', models.IntegerField(choices=[(0, 'Grid landing'), (1, 'Full screen sliding')], default=0)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language')),
            ],
            options={
                'verbose_name_plural': 'Default Settings',
                'verbose_name': 'Default Settings',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to=website.models.image_path)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('gallery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Category')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Photo')),
            ],
            options={
                'verbose_name_plural': 'Photos for category',
                'verbose_name': 'Photo for category',
            },
        ),
        migrations.CreateModel(
            name='PricePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('heading', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Language')),
            ],
            options={
                'verbose_name_plural': 'Price Page',
            },
        ),
        migrations.CreateModel(
            name='PricePagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_side_photo', models.BooleanField(default=False)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Photo', unique=True)),
                ('price_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.PricePage')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, max_length=100, null=True)),
                ('body', redactor.fields.RedactorField(blank=True, null=True, verbose_name='Question Body')),
                ('pricepage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.PricePage')),
            ],
        ),
        migrations.CreateModel(
            name='Question_FaqPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, max_length=100, null=True)),
                ('body', redactor.fields.RedactorField(blank=True, null=True, verbose_name='Question Body')),
                ('faqpage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.FaqPage')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', redactor.fields.RedactorField(verbose_name='Review')),
                ('author', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_side_photo', models.BooleanField(default=False)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Photo')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Review')),
            ],
        ),
        migrations.AddField(
            model_name='gallerybylanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
        migrations.AddField(
            model_name='faqphoto',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Photo', unique=True),
        ),
        migrations.AddField(
            model_name='faqpage',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
        migrations.AddField(
            model_name='contactspagephoto',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Photo', unique=True),
        ),
        migrations.AddField(
            model_name='contactspage',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
        migrations.AddField(
            model_name='categorybylanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
        migrations.AddField(
            model_name='aboutpagephoto',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Photo', unique=True),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Language', unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='photocategory',
            unique_together=set([('photo', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='gallerybylanguage',
            unique_together=set([('gallery', 'language')]),
        ),
    ]
