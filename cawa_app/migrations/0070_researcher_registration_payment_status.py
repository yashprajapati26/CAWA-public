# Generated by Django 2.0 on 2021-03-12 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0069_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher_registration',
            name='Payment_Status',
            field=models.BooleanField(default=False),
        ),
    ]