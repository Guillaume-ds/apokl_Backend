# Generated by Django 4.0.2 on 2022-03-16 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='list_nfts',
        ),
    ]
