from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id','ad_name','end_date','created_at']
    
    def location_name(self, obj):
        obj.locations.location_name
        
@admin.register(Location)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id','location_name','max_daily_visitors']
    
    def location_name(self, obj):
        obj.locations.location_name


@admin.register(DailyVisitorCount)
class DailyVisitorCountAdmin(admin.ModelAdmin):
    list_display = ['id','today_date','location','advertisement','visitor_count']
    
    def location_name(self, obj):
        obj.locations.location_name