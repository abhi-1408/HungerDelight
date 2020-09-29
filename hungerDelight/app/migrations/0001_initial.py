# Generated by Django 3.1.1 on 2020-09-29 13:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=6, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('lat', models.DecimalField(decimal_places=15, max_digits=18, verbose_name='latitude')),
                ('lng', models.DecimalField(decimal_places=15, max_digits=18, verbose_name='longitude')),
                ('operational', models.BooleanField()),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.merchant')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalAmount', models.DecimalField(decimal_places=6, max_digits=19)),
                ('total_items', models.PositiveIntegerField()),
                ('timeStamp', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('AWAITING', 'Awaiting'), ('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='SUCCESS', max_length=100)),
                ('paymentMode', models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'Card'), ('WALLET', 'Wallet'), ('NET BANKING', 'Net Banking')], default='CASH', max_length=255)),
                ('items', models.ManyToManyField(to='app.Item')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.merchant')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.store')),
            ],
        ),
    ]
