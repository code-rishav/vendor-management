# Generated by Django 4.2.7 on 2023-12-06 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0005_alter_vendor_average_response_time_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="vendor", name="password",),
    ]
