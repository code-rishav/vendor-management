# Generated by Django 4.2.7 on 2023-11-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_alter_purchaseorder_delivery_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseorder",
            name="acknowledgment_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(null=True),
        ),
    ]
