# Generated by Django 2.0.5 on 2018-06-22 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_moreuserdata_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Event Name'),
        ),
    ]