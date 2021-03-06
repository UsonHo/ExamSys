# Generated by Django 2.2.3 on 2019-12-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicapp', '0004_topicinfo_aid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('cur_type', models.BooleanField(choices=[(0, 'text_con'), (1, 'image_con'), (2, 'audio_con')], default=0, help_text='答题类型', verbose_name='答题类型')),
            ],
            options={
                'verbose_name': '选择题类型',
                'verbose_name_plural': '选择题类型',
            },
        ),
        migrations.CreateModel(
            name='FillBankType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('cur_type', models.BooleanField(choices=[(0, 'text_con'), (1, 'image_con'), (2, 'audio_con')], default=0, help_text='答题类型', verbose_name='答题类型')),
            ],
            options={
                'verbose_name': '填空题类型',
                'verbose_name_plural': '填空题类型',
            },
        ),
        migrations.AddField(
            model_name='choicesub',
            name='audio_url',
            field=models.CharField(help_text='音频', max_length=100, null=True, verbose_name='音频'),
        ),
        migrations.AddField(
            model_name='choicesub',
            name='image_url',
            field=models.CharField(help_text='图片', max_length=100, null=True, verbose_name='图片'),
        ),
        migrations.AddField(
            model_name='fillbanksub',
            name='audio_url',
            field=models.CharField(help_text='音频', max_length=100, null=True, verbose_name='音频'),
        ),
        migrations.AddField(
            model_name='fillbanksub',
            name='image_url',
            field=models.CharField(help_text='图片', max_length=100, null=True, verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='choicesub',
            name='title',
            field=models.CharField(help_text='题目', max_length=100, unique=True, verbose_name='选择-题目'),
        ),
        migrations.AlterField(
            model_name='fillbanksub',
            name='title',
            field=models.CharField(help_text='题目', max_length=100, unique=True, verbose_name='填空-题目'),
        ),
        migrations.DeleteModel(
            name='SubjectType',
        ),
        migrations.AddField(
            model_name='fillbanktype',
            name='sub',
            field=models.ManyToManyField(to='topicapp.FillbankSub'),
        ),
        migrations.AddField(
            model_name='choicetype',
            name='sub',
            field=models.ManyToManyField(to='topicapp.ChoiceSub'),
        ),
    ]
