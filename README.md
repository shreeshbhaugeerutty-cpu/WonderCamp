WonderCamp

### Pending booking expiry

Unpaid pending bookings reserve dates for 48 hours from creation. Once expired,
they remain in My Bookings under Expired and cannot be paid or modified.
Availability and booking/payment views enforce expiry when accessed, so dates
are released even when a scheduled cleanup is not running.

For background cleanup, schedule `python manage.py expire_bookings` every minute
using the deployment's scheduler and project virtual environment. Existing
pending bookings use their original creation time; those already 48 hours old
will expire on the next check. Paid bookings are preserved.
