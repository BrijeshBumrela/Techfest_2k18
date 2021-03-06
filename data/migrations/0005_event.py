# Generated by Django 2.0.5 on 2018-06-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20180622_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Event Name')),
                ('start_date_time', models.DateTimeField(verbose_name='Event Starts On ')),
                ('end_date_time', models.DateTimeField(verbose_name='Event Concludes On ')),
                ('description', models.TextField(verbose_name='Description')),
                ('rules', models.TextField(verbose_name='Contest Rules')),
                ('prize', models.TextField(verbose_name='Prize Description')),
                ('organisers', models.ManyToManyField(related_name='organising_events', to='data.MoreUserData')),
                ('participants', models.ManyToManyField(related_name='participating_events', to='data.MoreUserData')),
            ],
        ),
    ]
