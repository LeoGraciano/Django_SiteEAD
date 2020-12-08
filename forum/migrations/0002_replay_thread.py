# Generated by Django 3.1.3 on 2020-12-01 06:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='replay',
            name='thread',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='replays', to='forum.thread', verbose_name='Tropico'),
            preserve_default=False,
        ),
    ]
