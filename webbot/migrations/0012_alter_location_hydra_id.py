# Generated by Django 5.0.2 on 2024-03-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbot', '0011_zayavka_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='hydra_id',
            field=models.BigIntegerField(),
        ),
    ]
