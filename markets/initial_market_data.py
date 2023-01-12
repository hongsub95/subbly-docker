from markets.models import Market
from users.models import User


def gen_market(apps, schema_editor):

    Market(name="형아네옷가게", market_url="https://www.abc1.co.kr",  master_id=User.objects.filter(username="test2@test.com").first().id, description='형아네와 함께 멋진 스타일을 완성해보세요. #간편한 룩 #2030 #판교').save()
    Market(name="누나네옷가게", market_url="https://www.abc2.co.kr", master_id=User.objects.filter(username="test3@test.com").first().id, description='편한 스타일링을 추구합니다. #일상 #미니멀 #VLOG').save()

    market3: Market = Market(name="이모네옷가게", market_url="https://www.abc3.co.kr", master_id=User.objects.filter(username="test4@test.com").first().id, description='화려한 스타일을 추구합니다. #페북여신 #인스타여신')
    market3.save()

    market3.description = "화려한 스타일을 추구합니다. #인스타여신 #트위터여신 #판교"
    market3.save()