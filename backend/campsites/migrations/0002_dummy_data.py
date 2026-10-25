from django.db import migrations

PITCHES = [
    ('Hillside G-07', 'RIVERSIDE', 'Stunning views of the valley with direct sunrise exposure.',
     'images/PHOTO-2026-09-27-09-58-01.jpeg', 2800, 4, 1, 2, 2),
    ('Lakeside Loft', 'FOREST', 'Close to the dock, perfect for morning swims and canoe access.',
     'images/Rectangle@2x.png', 3500, 6, 2, 0, 2),
    ('Mountain Wild', 'FOREST', 'Secluded higher up, absolute peace and starry nights.',
     'images/Rectangle.png', 2500, 8, 2, 2, 3),
    ('Streamside Birch', 'RIVERSIDE', 'Listen to the soft rustle of the stream. Highly shaded.',
     'images/Rectangles.png', 4800, 5, 1, 1, 2),
]


def add_dummy_data(apps, schema_editor):
    Campsite = apps.get_model('campsites', 'Campsite')
    Pitch = apps.get_model('campsites', 'Pitch')

    campsites = [
        Campsite.objects.create(id=76, name='Bois Chéri Private Camp', location='Bois Chéri'),
        Campsite.objects.create(id=77, name='Black River Campsite', location='Black River'),
    ]

    for campsite in campsites:
        for p in PITCHES:
            Pitch.objects.create(
                campsite=campsite, name=p[0], category=p[1], description=p[2],
                image=p[3], price_per_night=p[4], max_campers=p[5],
                max_vehicles=p[6], max_pets=p[7], max_tents=p[8],
            )


def remove_dummy_data(apps, schema_editor):
    apps.get_model('campsites', 'Pitch').objects.all().delete()
    apps.get_model('campsites', 'Campsite').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('campsites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_dummy_data, remove_dummy_data),
    ]
