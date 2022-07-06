# Generated by Django 4.0.1 on 2022-03-02 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0002_alter_market_options'),
        ('clothes', '0004_alter_clothes_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='market',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clothes', to='markets.market', verbose_name='사이트'),
        ),
    ]
