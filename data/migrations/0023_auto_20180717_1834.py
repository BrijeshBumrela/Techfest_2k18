# Generated by Django 2.0.5 on 2018-07-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0022_auto_20180708_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='format',
            field=models.TextField(blank=True, max_length=500, verbose_name='Format'),
        ),
        migrations.AddField(
            model_name='event',
            name='prerequisites',
            field=models.TextField(blank=True, max_length=500, verbose_name='Pre-Requisites'),
        ),
        migrations.AddField(
            model_name='event',
            name='resources',
            field=models.TextField(blank=True, max_length=500, verbose_name='Resources'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, max_length=500, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='prize',
            field=models.TextField(blank=True, max_length=500, verbose_name='Prize Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='rules',
            field=models.TextField(blank=True, max_length=500, verbose_name='Contest Rules'),
        ),
    ]
