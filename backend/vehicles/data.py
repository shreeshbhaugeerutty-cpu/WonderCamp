RVS = [
    {
        "id": 1,
        "slug": "class-a",
        "name": "Class A Motorhomes RV",
        "subtitle": "High luxury RV",
        "image": "images/rv1.png",
        "price": 16500,
        "capacity": "6 - 8 persons",
        "phone": "23057100001",
        "amenities": ["Full kitchen", "Shower & toilet", "Air conditioning", "Queen bed", "Solar panels", "Smart TV"],
        "ratings": {
            "Comfort": 4.9,
            "Driving": 4.4,
            "Value": 4.1,
            "Cleanliness": 4.7,
            "Service": 4.8,
            "Sleep Quality": 4.9,
        },
        "reviews": [
            {"name": "Sarah Jenkins", "rating": 5.0, "text": "Absolute luxury on wheels! Super spacious and modern."},
            {"name": "David Miller", "rating": 5.0, "text": "Drove across the coast smoothly. Worth every rupee."},
            {"name": "Elena Rostova", "rating": 4.0, "text": "Great experience, very clean interior and comfy beds."},
        ],
    },
    {
        "id": 2,
        "slug": "class-b",
        "name": "Class B Motorhomes RV",
        "subtitle": "Medium luxury RV",
        "image": "images/rv2.png",
        "price": 12000,
        "capacity": "2 - 4 persons",
        "phone": "23057100002",
        "amenities": ["Kitchenette", "Fridge", "Outdoor shower", "Double bed", "Awning"],
        "ratings": {
            "Comfort": 4.2,
            "Driving": 4.9,
            "Value": 4.5,
            "Cleanliness": 4.3,
            "Service": 4.4,
            "Sleep Quality": 4.1,
        },
        "reviews": [
            {"name": "Mark Spencer", "rating": 5.0, "text": "Easy to park and drive. Perfect size for small families."},
            {"name": "Chloe Bennett", "rating": 4.0, "text": "Very reliable camper van with great fuel efficiency."},
        ],
    },
    {
        "id": 3,
        "slug": "class-c",
        "name": "Class C Motorhomes RV",
        "subtitle": "Medium luxury RV",
        "image": "images/rv3.png",
        "price": 7800,
        "capacity": "4 - 6 persons",
        "phone": "23057100003",
        "amenities": ["Kitchen", "Shower & toilet", "Bunk beds", "Large water tank", "Bike rack"],
        "ratings": {
            "Comfort": 4.5,
            "Driving": 4.2,
            "Value": 4.8,
            "Cleanliness": 4.6,
            "Service": 4.1,
            "Sleep Quality": 4.4,
        },
        "reviews": [
            {"name": "Thor Odinson", "rating": 5.0, "text": "Comfortable living while still being connected to mother nature."},
            {"name": "Tony Stark", "rating": 5.0, "text": "Top-tier luxury and smooth driving setup for high-end camping."},
            {"name": "Steve Rogers", "rating": 4.0, "text": "Exceptionally reliable vehicle with great sleeping arrangements."},
            {"name": "Natasha Romanoff", "rating": 4.0, "text": "Super clean interior, huge water capacity, and cozy beds."},
        ],
    },
]

# Quick lookups used by the detail page.
RVS_BY_SLUG = {rv["slug"]: rv for rv in RVS}
RVS_BY_ID = {rv["id"]: rv for rv in RVS}