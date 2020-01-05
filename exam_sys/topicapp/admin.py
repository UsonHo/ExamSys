from django.contrib import admin
from topicapp.models import ChoiceType, FillBankType, ChoiceSub, FillbankSub, TopicInfo

# Register your models here.

'''第二种方式：关联注册,必须是ForeignKey关联的类才可以'''
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin
'''
class ChoiceSubInline(admin.StackedInline):
    model = ChoiceSub


class FillbankSubInline(admin.StackedInline):
    model = FillbankSub


class TopicTypeInline(admin.StackedInline):
    model = TopicType


class TopicInfoInline(admin.StackedInline):
    model = TopicInfo
'''

'''装饰器方式单表注册'''


@admin.register(ChoiceType)
class SubjectTypeAdmin(admin.ModelAdmin):
    # inlines = [ChoiceSubInline, FillbankSubInline, TopicTypeInline, TopicInfoInline]
    inlines = []


admin.site.register(ChoiceSub)
admin.site.register(TopicInfo)
admin.site.register(FillbankSub)
admin.site.register(FillBankType)
