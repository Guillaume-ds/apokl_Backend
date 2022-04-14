# Generated by Django 4.0.2 on 2022-04-04 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0009_creator_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='picture',
            field=models.ImageField(default='', upload_to='photos/collection/<django.db.models.fields.CharField>_<django.db.models.fields.CharField>'),
        ),
        migrations.AlterField(
            model_name='creator',
            name='picture',
            field=models.ImageField(default='', upload_to='photos/creator/<django.db.models.fields.CharField>'),
        ),
    ]
