# Generated by Django 5.0.7 on 2024-08-19 06:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableForShippingRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='OrderContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=128)),
                ('lastname', models.CharField(max_length=128)),
                ('phoneNumber', models.IntegerField()),
                ('email', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=256)),
                ('zipCode', models.IntegerField()),
                ('city', models.CharField(max_length=256)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.availableforshippingregion')),
            ],
        ),
        migrations.CreateModel(
            name='PayCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=128)),
                ('checkout_id', models.CharField(default=None, max_length=512, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('shipping_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('status', models.CharField(choices=[('UNPAID', 'Unpaid'), ('PENDING', 'Pending'), ('DELIVERING', 'Delivering'), ('DELIVERED', 'Delivered')], default='UNPAID', max_length=10)),
                ('cart', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.cart')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('address', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.orderaddress')),
                ('contact', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.ordercontact')),
                ('paycheck', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.paycheck')),
            ],
        ),
    ]
