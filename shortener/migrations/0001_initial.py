import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="URLMap",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("original_url", models.URLField(max_length=2048)),
                ("hash", models.CharField(max_length=8, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "expires_at",
                    models.DateTimeField(
                        default=datetime.datetime(2025, 4, 27, 0, 17, 40, 635114, tzinfo=datetime.timezone.utc)
                    ),
                ),
            ],
        ),
    ]
