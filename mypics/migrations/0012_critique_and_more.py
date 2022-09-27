# Generated by Django 4.0.4 on 2022-09-04 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0011_rename_offending_user_query_user_making_recommendation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Critique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_making_recommendation', models.CharField(default=None, max_length=120)),
                ('details', models.TextField(default=None)),
            ],
        ),
        migrations.RenameField(
            model_name='query',
            old_name='user_making_recommendation',
            new_name='offending_user',
        ),
        migrations.AddField(
            model_name='query',
            name='picture_name',
            field=models.CharField(blank=True, default=None, max_length=120),
        ),
        migrations.AddField(
            model_name='query',
            name='song_name',
            field=models.CharField(blank=True, default=None, max_length=120),
        ),
        migrations.AddField(
            model_name='query',
            name='user_filing_complaint',
            field=models.CharField(default=None, max_length=120),
        ),
    ]
