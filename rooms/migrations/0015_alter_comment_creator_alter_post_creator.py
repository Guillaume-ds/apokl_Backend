# Generated by Django 4.0.2 on 2022-05-06 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0024_alter_collection_picture'),
        ('rooms', '0014_alter_comment_creator_alter_post_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='creators.creator'),
        ),
        migrations.AlterField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='creators.creator'),
        ),
    ]