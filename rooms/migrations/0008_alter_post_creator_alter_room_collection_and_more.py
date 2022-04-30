# Generated by Django 4.0.2 on 2022-04-30 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0022_alter_collection_creator'),
        ('rooms', '0007_alter_post_picture_alter_post_picture2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='creators.creator'),
        ),
        migrations.AlterField(
            model_name='room',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='creators.collection'),
        ),
        migrations.AlterField(
            model_name='room',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='creators.creator'),
        ),
    ]