# Generated by Django 4.2.2 on 2023-07-03 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo_app", "0002_project_capacity_project_technology_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="project_code",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]