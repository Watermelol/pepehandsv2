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

class commentAdmin(admin.ModelAdmin):
    list_display = ('Text', 'profit_tag', 'asset_tag', 'cash_tag', 'liquidity_tag')

class suggestionAdmin(admin.ModelAdmin):
    list_display = ('Text', 'profit_tag', 'asset_tag', 'cash_tag', 'liquidity_tag')

class profitTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_result', 'max_result', 'desc')

class assetTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_result', 'max_result', 'desc')

class cashTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_result', 'max_result', 'desc')

class liquidityTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_result', 'max_result', 'desc')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(user_profile)
admin.site.register(industries)
admin.site.register(user_financial_data_v2)
admin.site.register(tag_profit, profitTagAdmin)
admin.site.register(tag_asset, assetTagAdmin)
admin.site.register(tag_cash, cashTagAdmin)
admin.site.register(tag_liquidity, liquidityTagAdmin)
admin.site.register(Advices, suggestionAdmin)
admin.site.register(Comment, commentAdmin)
admin.site.register(Network_Suggestions)
admin.site.register(Recommandation_Video)
admin.site.register(Recommandation_Articles)
admin.site.register(user_payment)
admin.site.register(purchased_report)
admin.site.register(user_financial_data_analysis)

