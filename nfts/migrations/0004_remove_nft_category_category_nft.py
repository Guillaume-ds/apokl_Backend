# Generated by Django 4.0.2 on 2022-02-15 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfts', '0003_remove_category_nft_nft_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nft',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='NFT',
            field=models.ManyToManyField(to='nfts.NFT'),
        ),
    ]