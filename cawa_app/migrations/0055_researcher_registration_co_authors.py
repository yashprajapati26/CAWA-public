# Generated by Django 2.2 on 2021-03-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0054_researcher_registration_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher_registration',
            name='co_authors',
            field=models.CharField(default='cawa', max_length=100),
        ),
    ]
