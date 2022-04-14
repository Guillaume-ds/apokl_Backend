# Generated by Django 4.0.2 on 2022-02-15 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfts', '0002_remove_category_ordinal_remove_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='NFT',
        ),
        migrations.AddField(
            model_name='nft',
            name='category',
            field=models.ManyToManyField(default='Apokl', to='nfts.Category'),
        ),
    ]
