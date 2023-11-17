# Generated by Django 4.2.7 on 2023-11-17 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_hotel_price_max_hotel_price_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='totalroom',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_room', to='app1.hotel'),
        ),
    ]
