# Generated by Django 4.0.2 on 2022-06-22 13:34

from django.db import migrations, models
import django.db.models.deletion
import postsAndComments.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collectionsNft', '0001_initial'),
        ('profiles', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, default='', max_length=2000, upload_to=postsAndComments.models.post_directory_path)),
                ('picture2', models.ImageField(blank=True, default='', max_length=2000, upload_to=postsAndComments.models.post_directory_path)),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='collectionsNft.collection')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='profiles.profile')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='profiles.profile')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='postsAndComments.post')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
