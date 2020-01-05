from django.contrib import admin

from matchapp.models import MatchConfig, MatchReport
# Register your models here.

'''第二种方式：关联注册,必须是ForeignKey关联的类才可以'''
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin

'''
class MatchReportInline(admin.StackedInline):
    model = MatchReport


class MatchConfigAdmin(admin.ModelAdmin):
    inlines = [MatchReportInline]

admin.site.register(MatchConfig, MatchConfigAdmin)
'''
admin.site.register(MatchConfig)
admin.site.register(MatchReport)
