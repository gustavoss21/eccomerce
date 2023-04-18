from itertools import product
from django.contrib import admin
from . import models
# Register your models here.


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'curt_descrition',
                    'get_cost_formated', 'get_cost_promotion_formated']
    inlines = [
        VariacaoInline
    ]


admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
