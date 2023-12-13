from django.db import transaction
from rest_framework.response import Response
from .models import Advertisement, Location, DailyVisitorCount
from django.db.models import F, Q
from django.utils import timezone


def check_visitor_count(location_id):
    try:
        location = Location.objects.get(id=location_id) 
        print(f'Visitor Count: {location.visitor_count}, Max Daily Visitors: {location.max_daily_visitors}')
        print('------------------------->>>>>>>> Enter in TRY')
        if location.visitor_count >= location.max_daily_visitors or location.advertisements.filter(end_date__lt=timezone.now()).exists():
            print('-------------->>>>>>>>True')
            Advertisement.objects.filter(locations__id=location_id).update(ad_blocked=True)
        elif location.visitor_count < location.max_daily_visitors:
            print('-------------->>>>>>>>False')
            location.visitor_count += 1
            location.save()
    except Location.DoesNotExist:
        return Response({'msg': f'Record with the location ID {location_id} does not exist'})


def create_daily_visitor_counts(location_id):
    try:
        with transaction.atomic():
            ads = Advertisement.objects.filter(Q(locations__id=location_id) & Q(ad_blocked=False))
            daily_visitor_counts = [
                DailyVisitorCount(
                    today_date=timezone.now(),
                    location_id=location_id,
                    advertisement_id=ad.id,
                    visitor_count=ad.locations.get(id=location_id).visitor_count
                )
                for ad in ads
            ]
            DailyVisitorCount.objects.bulk_create(daily_visitor_counts)

        return {'msg': 'DailyVisitorCount records created successfully'}
    except Location.DoesNotExist:
        return {'msg': f'Record with the location ID {location_id} does not exist'}
    except Exception as e:
        return {'msg': str(e)}