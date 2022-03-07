# Generated by Django 2.2 on 2021-03-03 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0050_delete_co_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Co_author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='Mr.', max_length=10)),
                ('Firstname', models.CharField(max_length=50)),
                ('Lastname', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('Phone', models.BigIntegerField()),
                ('Institute', models.CharField(max_length=50)),
                ('Address', models.TextField(max_length=150)),
                ('Designation', models.CharField(max_length=50)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cawa_app.RegCategory')),
                ('Researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cawa_app.Researcher_registration')),
            ],
        ),
    ]