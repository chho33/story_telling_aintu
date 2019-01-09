# Generated by Django 2.1.3 on 2019-01-09 03:44

import audiofield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tags', models.CharField(max_length=200)),
                ('parse', models.CharField(max_length=500)),
                ('upload_at', models.DateTimeField(auto_now_add=True)),
                ('audio_file', audiofield.fields.AudioField(blank=True, help_text='Allowed type - .mp3, .wav, .ogg', upload_to='audio')),
            ],
            options={
                'verbose_name': 'audio file',
                'verbose_name_plural': 'audio files',
                'default_permissions': ('add', 'change', 'delete'),
            },
        ),
    ]