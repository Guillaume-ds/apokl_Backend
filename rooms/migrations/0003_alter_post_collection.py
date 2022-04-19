# Generated by Django 4.0.2 on 2022-04-19 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0014_creator_discordurl_creator_instagramurl_and_more'),
        ('rooms', '0002_remove_room_stars_room_adresses_room_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='creators.collection'),
        ),
    ]