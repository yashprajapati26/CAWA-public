# Generated by Django 2.0 on 2021-02-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0039_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Title',
            field=models.CharField(default='Mr.', max_length=10),
        ),
    ]
