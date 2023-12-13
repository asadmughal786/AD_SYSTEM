from django.db import models


# Create your models here.


class Location(models.Model):
    location_name = models.CharField(max_length=255, blank=True, null=False)
    max_daily_visitors = models.PositiveIntegerField(default=0)
    visitor_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Locations'
        
    def __str__(self):
        return self.location_name

class Advertisement(models.Model):
    ad_name = models.CharField(max_length=255, blank=True, null=False)
    end_date = models.DateTimeField()
    locations = models.ManyToManyField('Location', related_name='advertisements')
    ad_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Advertisements'
        
    def __str__(self):
        return self.ad_name
    

class DailyVisitorCount(models.Model):
    today_date = models.DateTimeField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, blank=True)
    visitor_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Daily Visitor Count'