# Generated by Django 5.1.6 on 2025-02-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
