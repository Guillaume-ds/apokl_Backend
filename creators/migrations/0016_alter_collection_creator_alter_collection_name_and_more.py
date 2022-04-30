# Generated by Django 4.0.2 on 2022-04-28 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0015_alter_collection_options_alter_creator_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='creators.creator'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.CharField(default='Atest', max_length=500, unique=True),
        ),
    ]
