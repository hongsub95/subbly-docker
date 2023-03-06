# Generated by Django 4.1rc1 on 2023-03-03 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_address_order_coupon_order_deleted_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paycate',
            field=models.CharField(choices=[('card', '카드'), ('cash', '계좌이체')], default='cash', max_length=10),
        ),
    ]