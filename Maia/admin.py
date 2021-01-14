from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = user_profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(user_profile)
admin.site.register(industries)
admin.site.register(user_financial_data)
admin.site.register(tag)
admin.site.register(Advices)
admin.site.register(Comment)
admin.site.register(Network_Suggestions)
admin.site.register(Recommandation_Video)
admin.site.register(Recommandation_Articles)
admin.site.register(user_payment)
admin.site.register(purchased_report)

