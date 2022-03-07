# Generated by Django 2.0 on 2021-03-08 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0066_auto_20210308_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abstract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PaperID', models.IntegerField()),
                ('Title', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('File', models.FileField(default='Abc.pdf', upload_to='files/')),
                ('Registration_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cawa_app.Researcher_registration')),
            ],
        ),
    ]