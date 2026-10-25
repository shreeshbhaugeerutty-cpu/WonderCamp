

# Create your views here.
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.http import require_POST

SPOTS = [
    (1, "Chamarel Seven Coloured Earth", "sightseeing", -20.4419, 57.3746, "Stunning geological formation of dunes.", "Chamarel Seven Coloured Earths Mauritius.jpg"),
    (2, "Black River Gorges", "nature", -20.3833, 57.4333, "Mauritius' largest national park with waterfalls.", "Black River Gorges National Park Mauritius waterfall.jpg"),
    (3, "Le Morne Brabant", "beaches", -20.4525, 57.3128, "UNESCO World Heritage mountain and lagoon.", "Le Morne Brabant.jpg"),
    (4, "Underwater Waterfall", "adventure", -20.4700, 57.3200, "Breathtaking optical illusion best seen from a helicopter.", "underwater-waterfall-mauritius (4).jpg"),
    (5, "Pamplemousses Botanical Garden", "sightseeing", -20.1046, 57.5808, "Historic garden with giant water lilies.", "112122-Pamplemoose-Mauritius-18-of-31.jpg"),
    (6, "Grand Bassin", "sightseeing", -20.4172, 57.4931, "Sacred crater lake and Hindu temples.", "grand-bassin-mauritius-hg77.avif"),
]


def map_view(request):
    spots = [
        {
            "id": i,
            "name": n,
            "category": c,
            "lat": la,
            "lng": lo,
            "blurb": b,
            "image": f"wondercamp/img/{img}",
            "image_url": static(f"wondercamp/img/{img}"),
            "url": "#",
        }
        for i, n, c, la, lo, b, img in SPOTS
    ]
    return render(request, "maps/map.html", {"spots": spots[:4], "spots_json": spots})


def sos_view(request):
    return render(request, "sos.html")


@require_POST
def sos_trigger(request):
    data = json.loads(request.body or "{}")
    print("SOS received:", data)  # TODO: save alert, notify staff / SMS gateway
    return JsonResponse({"status": "sent"})