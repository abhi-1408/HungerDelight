# Generated by Django 3.1.1 on 2020-10-01 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='paymentMode',
            new_name='payment_mode',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='timeStamp',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='totalAmount',
            new_name='total_amount',
        ),
    ]