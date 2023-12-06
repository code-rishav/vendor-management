# Generated by Django 4.2.7 on 2023-12-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vendor",
            fields=[
                ("name", models.CharField(max_length=100)),
                ("contact_details", models.TextField()),
                ("address", models.TextField()),
                (
                    "vendor_code",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("on_time_delivery_rate", models.FloatField(default=0.0, null=True)),
                ("quality_rating_avg", models.FloatField(default=0.0, null=True)),
                ("average_response_time", models.FloatField(default=0.0, null=True)),
                ("fulfillment_rate", models.FloatField(default=0.0, null=True)),
            ],
        ),
    ]