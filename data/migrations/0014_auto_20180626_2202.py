# Generated by Django 2.0.5 on 2018-06-26 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_eventcatalogue'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcatalogue',
            options={'ordering': ['-event']},
        ),
    ]