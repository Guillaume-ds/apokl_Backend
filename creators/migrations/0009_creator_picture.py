# Generated by Django 4.0.2 on 2022-04-04 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0008_alter_creator_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='creator',
            name='picture',
            field=models.ImageField(default='', upload_to='photos/<django.db.models.fields.CharField>'),
        ),
    ]