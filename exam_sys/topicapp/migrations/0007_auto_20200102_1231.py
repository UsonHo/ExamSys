# Generated by Django 2.2.3 on 2020-01-02 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicapp', '0006_auto_20191223_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicesub',
            name='perSore',
            field=models.SmallIntegerField(default=1, help_text='本题分数', verbose_name='本题分数'),
        ),
        migrations.AddField(
            model_name='fillbanksub',
            name='perSore',
            field=models.SmallIntegerField(default=1, help_text='本题分数', verbose_name='本题分数'),
        ),
    ]
