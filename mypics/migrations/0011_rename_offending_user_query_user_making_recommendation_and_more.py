# Generated by Django 4.0.4 on 2022-09-04 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0010_alter_query_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='offending_user',
            new_name='user_making_recommendation',
        ),
        migrations.RemoveField(
            model_name='query',
            name='picture_name',
        ),
        migrations.RemoveField(
            model_name='query',
            name='song_name',
        ),
        migrations.RemoveField(
            model_name='query',
            name='user_filing_complaint',
        ),
    ]