# Generated by Django 2.2.3 on 2020-01-03 08:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0016_auto_20200102_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverify',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 3, 16, 10, 48, 689912), verbose_name='发送时间'),
        ),
    ]