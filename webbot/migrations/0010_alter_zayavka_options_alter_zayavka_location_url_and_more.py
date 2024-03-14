# Generated by Django 5.0.2 on 2024-03-11 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbot', '0009_alter_agent_options_zayavka'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zayavka',
            options={},
        ),
        migrations.AlterField(
            model_name='zayavka',
            name='location_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='zayavka',
            name='passport_back_image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='zayavka',
            name='passport_front_image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
