# Generated by Django 4.0.4 on 2022-09-14 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0013_help'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='date',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='picture',
            name='place',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='picture',
            name='title',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
