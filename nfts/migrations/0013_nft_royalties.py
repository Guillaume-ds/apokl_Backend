# Generated by Django 4.0.2 on 2022-05-03 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfts', '0012_nft_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='nft',
            name='royalties',
            field=models.IntegerField(default=0),
        ),
    ]