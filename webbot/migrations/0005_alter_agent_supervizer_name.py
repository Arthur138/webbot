# Generated by Django 5.0.2 on 2024-02-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbot', '0004_remove_agent_supervizer_surname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='supervizer_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
