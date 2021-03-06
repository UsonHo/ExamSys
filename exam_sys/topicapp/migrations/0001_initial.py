# Generated by Django 3.0 on 2019-12-12 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('title', models.CharField(help_text='题目', max_length=100, verbose_name='选择-题目')),
                ('answer', models.CharField(help_text='答案', max_length=100, verbose_name='答案')),
                ('radio1', models.CharField(help_text='选项一', max_length=32, null=True, verbose_name='选项一')),
                ('radio2', models.CharField(help_text='选项二', max_length=32, null=True, verbose_name='选项二')),
                ('radio3', models.CharField(help_text='选项三', max_length=32, null=True, verbose_name='选项三')),
                ('radio4', models.CharField(help_text='选项四', max_length=32, null=True, verbose_name='选项四')),
                ('source', models.CharField(help_text='题目来源', max_length=64, null=True, verbose_name='题目来源')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FillbankSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('title', models.CharField(help_text='题目', max_length=100, verbose_name='填空-题目')),
                ('answer', models.CharField(help_text='答案', max_length=100, verbose_name='答案')),
                ('source', models.CharField(help_text='题目来源', max_length=64, null=True, verbose_name='题目来源')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopicType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topictype', models.SmallIntegerField(choices=[(0, '技术类'), (1, '教育类'), (2, '文化类'), (3, '常识类'), (4, '地理类'), (5, '体育类'), (6, '面试类'), (7, '热门题库')], default=7, help_text='题库类型', verbose_name='题库类型')),
            ],
        ),
        migrations.CreateModel(
            name='TopicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qsize', models.SmallIntegerField(default=0, help_text='题库大小', verbose_name='题库大小')),
                ('qname', models.CharField(help_text='题库名', max_length=20, unique=True, verbose_name='题库名')),
                ('qselect', models.SmallIntegerField(default=0, help_text='选择题数', verbose_name='选择题数')),
                ('qfillblank', models.SmallIntegerField(default=0, help_text='填空题数', verbose_name='填空题数')),
                ('qucount', models.SmallIntegerField(default=0, help_text='参与人次', verbose_name='参与人次')),
                ('qhasmatch', models.SmallIntegerField(default=0, help_text='已出比赛数', verbose_name='已出比赛数')),
                ('chinfo', models.ManyToManyField(to='topicapp.ChoiceSub')),
                ('fbinfo', models.ManyToManyField(to='topicapp.FillbankSub')),
                ('qtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topicapp.TopicType')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('atype', models.BooleanField(choices=[(0, 'text_con'), (1, 'image_con'), (2, 'audio_con')], default=0, help_text='答题类型', verbose_name='答题类型')),
                ('choice', models.ManyToManyField(to='topicapp.ChoiceSub')),
                ('fillbank', models.ManyToManyField(to='topicapp.FillbankSub')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
