# Generated by Django 2.2 on 2021-02-04 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0021_auto_20210203_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewer',
            old_name='Reviwer_user',
            new_name='Reviewer_user',
        ),
    ]
