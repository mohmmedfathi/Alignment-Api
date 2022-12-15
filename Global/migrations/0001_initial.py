# Generated by Django 4.1.4 on 2022-12-15 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Global",
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
                ("seq1", models.CharField(max_length=100)),
                ("seq2", models.CharField(max_length=100)),
                ("aligned1", models.CharField(max_length=100)),
                ("aligned2", models.CharField(max_length=100)),
            ],
        ),
    ]
