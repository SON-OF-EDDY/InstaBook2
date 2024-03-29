# Generated by Django 4.0.4 on 2022-09-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0003_song_connected_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_filing_complaint', models.CharField(max_length=120)),
                ('offending_user', models.CharField(max_length=120)),
                ('picture_song_name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
