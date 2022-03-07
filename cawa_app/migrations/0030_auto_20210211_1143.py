# Generated by Django 2.0 on 2021-02-11 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0029_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='Abstract_Acceptance_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='conference',
            name='Abstract_Submission_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='conference',
            name='Conference_Description',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='conference',
            name='FullPaper_Acceptance_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='conference',
            name='FullPaper_Submission_Date',
            field=models.DateField(),
        ),
    ]
