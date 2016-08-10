# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-10 14:12
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20160809_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewByLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', redactor.fields.RedactorField(verbose_name='Review')),
                ('author', models.CharField(max_length=200)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Language')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewPagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_side_photo', models.BooleanField(default=False)),
                ('photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Photo')),
            ],
        ),
        migrations.RemoveField(
            model_name='reviewphoto',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='reviewphoto',
            name='review',
        ),
        migrations.RemoveField(
            model_name='aboutpagebylanguage',
            name='page_name_in_menu',
        ),
        migrations.RemoveField(
            model_name='contactspage',
            name='page_name_in_menu',
        ),
        migrations.RemoveField(
            model_name='faqpagebylanguage',
            name='page_name_in_menu',
        ),
        migrations.RemoveField(
            model_name='pricepagebylanguage',
            name='page_name_in_menu',
        ),
        migrations.RemoveField(
            model_name='retouchpagebylanguage',
            name='page_name_in_menu',
        ),
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='photos_order',
        ),
        migrations.RemoveField(
            model_name='review',
            name='review',
        ),
        migrations.RemoveField(
            model_name='reviewpagebylanguage',
            name='page_name_in_menu',
        ),
        migrations.AddField(
            model_name='review',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Photo'),
        ),
        migrations.AddField(
            model_name='reviewpage',
            name='photos_order',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True),
        ),
        migrations.AddField(
            model_name='reviewpagebylanguage',
            name='review_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.ReviewPage'),
        ),
        migrations.DeleteModel(
            name='ReviewPhoto',
        ),
        migrations.AddField(
            model_name='reviewpagephoto',
            name='review_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='website.ReviewPage'),
        ),
        migrations.AddField(
            model_name='reviewbylanguage',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Review'),
        ),
    ]
