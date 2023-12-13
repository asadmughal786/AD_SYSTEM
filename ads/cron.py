from django.utils import timezone
from .models import Advertisement, Location
import logging

logger = logging.getLogger(__name__)

def reset_the_visitor_counter():
    try:
        ads_to_update = Advertisement.objects.filter(end_date__gte=timezone.now())
        if ads_to_update.exists():
            ads_to_update.update(ad_blocked=False)
            logger.info('Ad blocked updated successfully')
        else:
            logger.info('No advertisements to update')

        if Location.objects.exists():
            Location.objects.all().update(visitor_count=0)
            logger.info('Visitor counts reset successfully')
        else:
            logger.info('No daily visitor counts to update')

        logger.info('Cron job executed successfully')

    except Exception as e:
        logger.error(f'Cron job failed: {str(e)}', exc_info=True)


# def print_hello():
#     print('hello')
#     logger.info('Cron job called')