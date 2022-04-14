# Generated by Django 4.0.2 on 2022-02-15 10:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(default='Artiste Anonyme', max_length=200)),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=150)),
                ('photo_main', models.ImageField(default='photos/default.jpg', upload_to='photos/%Y/%m/%d/')),
                ('description', models.TextField(blank=True)),
                ('sale_type', models.CharField(choices=[('Auction', 'Auction'), ('Fixed price', 'Fixed')], default='Fixed price', max_length=50)),
                ('blockchain', models.CharField(choices=[('Ethereum', 'Ethereum'), ('Polygon', 'Polygon'), ('Other', 'Other')], default='Ethereum', max_length=50)),
                ('price', models.IntegerField(default=1)),
                ('rarity', models.IntegerField(default=1)),
                ('is_published', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('ordinal', models.IntegerField()),
                ('NFT', models.ManyToManyField(to='nfts.NFT')),
            ],
        ),
    ]
