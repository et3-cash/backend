import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import OTP

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_otps():
    logger.info("Running delete_expired_otps task.")
    expiration_time = timezone.now() - timedelta(minutes=5)
    expired_otps = OTP.objects.filter(created_at__lt=expiration_time)
    count, _ = expired_otps.delete()
    logger.info(f"Deleted {count} expired OTP(s).")
