# Generated by Django 2.0 on 2021-02-27 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0044_co_author_researcher_registration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher_registration',
            name='Category',
        ),
        migrations.RemoveField(
            model_name='researcher_registration',
            name='Participant_users',
        ),
        migrations.DeleteModel(
            name='Researcher_registration',
        ),
    ]
