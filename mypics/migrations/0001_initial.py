# Generated by Django 4.0.4 on 2022-09-02 16:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mypics.models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('artist', models.CharField(max_length=120)),
                ('author', models.CharField(max_length=120)),
                ('song_file', models.FileField(upload_to='songs/')),
                ('connected_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('profile_pic', models.ImageField(null=True, upload_to='images/')),
                ('youtube_url', models.CharField(blank=True, max_length=120, null=True)),
                ('telegram_url', models.CharField(blank=True, max_length=120, null=True)),
                ('vk_url', models.CharField(blank=True, max_length=120, null=True)),
                ('friend_id_list', models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('requests', models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('pendings', models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('accepted', models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('declined', models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('private', models.BooleanField(blank=True, null=True)),
                ('member', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='', max_length=120)),
                ('title', models.CharField(max_length=120)),
                ('date', models.CharField(max_length=120)),
                ('place', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('picture_image', models.ImageField(null=True, upload_to='images/')),
                ('likes', models.CharField(default=0, max_length=120)),
                ('hearted', models.CharField(blank=True, default='', max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('connected_user', models.ForeignKey(default=mypics.models.get_default_action_status, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dialogue', models.TextField(blank=True)),
                ('member_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mypics.profile')),
                ('member_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mypics.profile')),
            ],
        ),
    ]
