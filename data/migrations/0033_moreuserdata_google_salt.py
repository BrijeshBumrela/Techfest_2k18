# Generated by Django 2.0.5 on 2018-08-12 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0032_moreuserdata_google_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='moreuserdata',
            name='google_salt',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]