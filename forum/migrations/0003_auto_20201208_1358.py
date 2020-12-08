# Generated by Django 3.1.3 on 2020-12-08 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_replay_thread'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField(verbose_name='Resposta')),
                ('correct', models.BooleanField(blank=True, default=False, verbose_name='Correta?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Resposta',
                'verbose_name_plural': 'Respostas',
                'ordering': ['-correct', 'created'],
            },
        ),
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['-modified'], 'verbose_name': 'Tópico', 'verbose_name_plural': 'Tópicos'},
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='answer',
            new_name='answers',
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='modified_at',
            new_name='modified',
        ),
        migrations.AlterField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='body',
            field=models.TextField(verbose_name='Mensagem'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Título'),
        ),
        migrations.DeleteModel(
            name='Replay',
        ),
        migrations.AddField(
            model_name='reply',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.thread', verbose_name='Tópico'),
        ),
    ]