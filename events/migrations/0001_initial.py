# Generated by Django 4.0.2 on 2022-06-22 13:34

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collectionsNft', '0001_initial'),
        ('profiles', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('addresses', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10000), blank=True, default=list, size=None)),
                ('users', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10000), blank=True, default=list, size=None)),
                ('picture2', models.ImageField(blank=True, default='', max_length=2000, upload_to=events.models.event_directory_path)),
                ('picture', models.ImageField(blank=True, default='', max_length=2000, upload_to=events.models.event_directory_path)),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='collectionsNft.collection')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='profiles.profile')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
