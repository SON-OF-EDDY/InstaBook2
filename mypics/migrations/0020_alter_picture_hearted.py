# Generated by Django 4.0.4 on 2022-09-30 09:54

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0019_alter_song_song_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='hearted',
            field=models.CharField(blank=True, default=None, max_length=120, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
