# Generated by Django 4.1rc1 on 2023-03-14 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupons', '0001_initial'),
        ('clothes', '0002_alter_clothes_options_alter_product_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('order_id', models.CharField(max_length=15, null=True)),
                ('orderstate', models.CharField(choices=[('complete', '배송완료'), ('shipping', '배송중'), ('purchase', '구매완료'), ('exchange', '교환')], default='purchase', max_length=20)),
                ('address', models.CharField(max_length=100, null=True, verbose_name='주소')),
                ('paycate', models.CharField(choices=[('card', '카드'), ('cash', '계좌이체')], default='cash', max_length=10)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='coupons.coupon')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='clothes.product')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
