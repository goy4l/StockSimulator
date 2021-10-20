from django.contrib import admin

from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from .models import league, stocks,news,holdings, transaction,transfer

admin.site.site_header = 'Xavage Administration'


@admin.register(league)
class leagueAdmin(admin.ModelAdmin):
    list_display = ("name", "game_code")

@admin.register(stocks)
class stockAdmin(admin.ModelAdmin):
    list_display = ('id',"name", "price")
    search_fields = ("name__startswith",)



@admin.register(news)
class newsAdmin(admin.ModelAdmin):
    list_display = ("title", "stock",'created_at')


@admin.register(holdings)
class holdingsAdmin(admin.ModelAdmin):
    list_display = ("user", "stock")
    list_filter = ("user",'stock')
    search_fields = ("user__startswith", 'stock__startswith')


@admin.register(transaction)
class transactionAdmin(admin.ModelAdmin):
    list_display = ("user", "stock",'quantity','buy_price','created_at')
    list_filter = ("user",'stock')
    search_fields = ("user__startswith", 'stock__startswith')

@admin.register(transfer)
class transferAdmin(admin.ModelAdmin):
    list_display = ("to_user", "from_user",'stock','quantity','status')
    list_filter = ("to_user",'stock','from_user')
    search_fields = ("to_user__startswith", 'stock__startswith',"from_user__startswith",)
