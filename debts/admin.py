from django.contrib import admin
from .models import Debtor, Transaction

@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('name','balance','created')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ('debtor','kind','amount','timestamp')
    list_filter   = ('kind',)
    search_fields = ('debtor__name',)
