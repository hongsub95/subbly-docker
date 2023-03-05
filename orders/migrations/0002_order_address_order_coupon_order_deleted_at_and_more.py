# Generated by Django 4.1rc1 on 2023-03-02 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=20, null=True, verbose_name='주소'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='coupons.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='삭제일'),
        ),
        migrations.AddField(
            model_name='order',
            name='paycate',
            field=models.CharField(choices=[('card', '카드'), ('cash', '현금')], default='cash', max_length=10),
        ),
    ]
