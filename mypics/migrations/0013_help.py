# Generated by Django 4.0.4 on 2022-09-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypics', '0012_critique_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_asking_help', models.CharField(default=None, max_length=120)),
                ('dialogue', models.TextField(blank=True, default=None)),
            ],
        ),
    ]