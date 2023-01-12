from django.db import migrations

from users.initial_user_data import gen_users
from markets.initial_market_data import gen_market
from clothes.initial_clothes_data import gen_clothes

class Migration(migrations.Migration):
    initial = True
    dependencies = [
    
    ]
    operations = [
        migrations.RunPython(gen_users),
        migrations.RunPython(gen_market),
        migrations.RunPython(gen_clothes)
    ]