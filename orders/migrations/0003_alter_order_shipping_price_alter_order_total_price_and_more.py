# Generated by Django 5.0.7 on 2024-08-22 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_paycheck_payer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_price',
            field=models.DecimalField(decimal_places=2, max_digits=64),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=64),
        ),
        migrations.AlterField(
            model_name='paycheck',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=64),
        ),
    ]
