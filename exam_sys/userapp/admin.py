from django.contrib import admin
from userapp.models import RegUser, AuthUser

# Register your models here.

'''第一种注册方式，没有自定义管理界面'''
admin.site.register(RegUser)
# admin.site.register(UserProfile)
# admin.site.register(AuthUser)

'''第一种注册方式，自定义管理界面'''
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('oname',)

admin.site.register(AuthUser, AuthUserAdmin)
