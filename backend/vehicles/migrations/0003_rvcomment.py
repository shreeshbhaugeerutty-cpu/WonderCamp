from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0002_remove_rvpricehistory_campsite_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="RVComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rv_slug", models.SlugField(max_length=100)),
                ("name", models.CharField(max_length=60)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (5, "5 - Excellent"),
                            (4, "4 - Very good"),
                            (3, "3 - Average"),
                            (2, "2 - Poor"),
                            (1, "1 - Terrible"),
                        ],
                        default=5,
                    ),
                ),
                ("text", models.TextField(max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]