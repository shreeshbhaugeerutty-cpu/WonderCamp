from django.core.management.base import BaseCommand

from backend.bookings.models import Booking


class Command(BaseCommand):
    help = 'Expire unpaid pending bookings older than 48 hours.'

    def handle(self, *args, **options):
        count = Booking.expire_pending()
        self.stdout.write(f'Expired {count} unpaid booking(s).')
