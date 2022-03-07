# Generated by Django 2.0 on 2021-03-18 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cawa_app', '0077_auto_20210318_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review_Abstract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(auto_now_add=True)),
                ('Status', models.CharField(default='pending', max_length=100)),
                ('Evaluation', models.CharField(blank=True, max_length=100)),
                ('Reviews', models.TextField()),
                ('Abstract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cawa_app.Abstract')),
                ('Reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cawa_app.Reviewer')),
            ],
        ),
    ]
