"""Shared booking settings for campsites and camping vans."""
import re

from backend.campsites.data import CAMPSITES_BY_SLUG
from backend.vehicles.data import RVS


VANS_BY_SLUG = {}
for rv in RVS:
    capacity = [int(value) for value in re.findall(r"\d+", rv['capacity'])]
    slug = 'rv-' + rv['slug']
    VANS_BY_SLUG[slug] = {
        **rv, 'slug': slug, 'rv_slug': rv['slug'], 'is_van': True,
        'location': 'Mauritius', 'min_campers': min(capacity),
        'max_campers': max(capacity), 'max_vehicles': 1,
        'max_pets': 0, 'min_tents': 0, 'max_tents': 0,
    }

BOOKABLES_BY_SLUG = {**CAMPSITES_BY_SLUG, **VANS_BY_SLUG}
