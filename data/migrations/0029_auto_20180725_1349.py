# Generated by Django 2.0.5 on 2018-07-25 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0028_auto_20180725_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='button1_title',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='button2_title',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]