# Generated by Django 2.2.3 on 2020-01-02 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchapp', '0005_auto_20191231_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchconfig',
            name='score',
        ),
    ]
