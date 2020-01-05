# Generated by Django 2.2.3 on 2019-12-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicapp', '0005_auto_20191223_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicetype',
            name='cur_type',
            field=models.SmallIntegerField(choices=[(0, 'text_con'), (1, 'image_con'), (2, 'audio_con')], default=0, help_text='答题类型', verbose_name='答题类型'),
        ),
        migrations.AlterField(
            model_name='fillbanktype',
            name='cur_type',
            field=models.SmallIntegerField(choices=[(0, 'text_con'), (1, 'image_con'), (2, 'audio_con')], default=0, help_text='答题类型', verbose_name='答题类型'),
        ),
    ]