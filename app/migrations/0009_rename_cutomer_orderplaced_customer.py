# Generated by Django 5.0.5 on 2024-07-27 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_payment_orderplaced'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderplaced',
            old_name='cutomer',
            new_name='customer',
        ),
    ]
