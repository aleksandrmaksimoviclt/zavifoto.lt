# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
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
            ],
        ),
        migrations.CreateModel(
            name='AboutPageByLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_text', models.TextField(blank=True, null=True)),
                ('main_text', models.TextField(blank=True, null=True)),
                ('bottom_text', models.TextField(blank=True, null=True)),
                ('about_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.AboutPage')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
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
            name='ContactsPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
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
                ('style', models.IntegerField(default=0)),
                ('layout', models.IntegerField(default=0)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=website.models.image_path)),
                ('category', models.ManyToManyField(to='website.Category')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='PricePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PricePageByLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_text', models.TextField(blank=True, null=True)),
                ('main_text', models.TextField(blank=True, null=True)),
                ('bottom_text', models.TextField(blank=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language')),
                ('pricepage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.PricePage')),
            ],
        ),
        migrations.AddField(
            model_name='gallerybylanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
        migrations.AddField(
            model_name='categorybylanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
        migrations.AddField(
            model_name='category',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Gallery'),
        ),
        migrations.AddField(
            model_name='aboutpagebylanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Language'),
        ),
    ]