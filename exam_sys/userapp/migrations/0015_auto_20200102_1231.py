# Generated by Django 2.2.3 on 2020-01-02 04:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0014_auto_20191231_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverify',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 2, 12, 31, 18, 654489), verbose_name='发送时间'),
        ),
    ]