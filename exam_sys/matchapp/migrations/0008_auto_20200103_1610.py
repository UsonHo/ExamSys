# Generated by Django 2.2.3 on 2020-01-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchapp', '0007_remove_matchreport_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchreport',
            name='usedtime',
            field=models.CharField(help_text='答题用时', max_length=20, verbose_name='答题用时'),
        ),
    ]
