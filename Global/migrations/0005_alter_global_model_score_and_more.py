# Generated by Django 4.1.4 on 2022-12-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Global", "0004_alter_global_model_score_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="global_model", name="score", field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="global_model",
            name="trace_back",
            field=models.TextField(null=True),
        ),
    ]