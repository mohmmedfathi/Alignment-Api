# Generated by Django 2.2.28 on 2023-01-03 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Global_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq1', models.CharField(max_length=100)),
                ('seq2', models.CharField(max_length=100)),
                ('aligned1', models.CharField(max_length=100)),
                ('aligned2', models.CharField(max_length=100)),
                ('score_matrix', models.TextField(null=True)),
                ('traceback_matrix', models.TextField(null=True)),
            ],
        ),
    ]
