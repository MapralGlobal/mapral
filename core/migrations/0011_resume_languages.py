# Generated by Django 4.1 on 2022-09-03 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_resume_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='languages',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
