# Generated by Django 4.0.4 on 2022-09-14 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0014_alter_picture_date_alter_picture_place_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
