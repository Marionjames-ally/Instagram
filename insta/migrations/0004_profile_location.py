# Generated by Django 3.0.3 on 2020-03-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0003_remove_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]