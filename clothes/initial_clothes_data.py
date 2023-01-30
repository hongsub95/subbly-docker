from . import models as clothes_models
from markets.models import Market
def gen_category():
    clothes_models.Categories(name="상의").save()
    clothes_models.Categories(name="하의").save()
    clothes_models.Categories(name="신발").save()
    clothes_models.Categories(name="원피스").save()
    clothes_models.Categories(name="아우터").save()

def gen_product(name,description,stock,price,clothes_colors,clothes_sizes,category,market,is_sold_out):
    category_id = clothes_models.Categories.objects.filter(name=category).first().id
    market_id = Market.objects.filter(name=market).first().id 
    clothes = clothes_models.Clothes(name=name,description=description,price=price,category_id=category_id,market_id=market_id,)
    clothes.save()
    for size in clothes_sizes:
        for color in clothes_colors:
            clothes_models.Product(
                clothes=clothes,
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category_id,
                market_id=market_id,
                size=size,
                colors =color,
                is_sold_out=is_sold_out).save()
    

def gen_clothes(apps, schema_editor):
    gen_category()
    
    #clothes1
    clothes1_colors = ("레드","블랙","화이트","네이비")
    clothes1_sizes = ("S","M","L","XL")
    gen_product("맨투맨1","요새 핫한 맨투맨",300,25000,clothes1_colors,clothes1_sizes,"상의","누나네옷가게",False)
    
    #clothes2
    clothes2_colors = ("블랙","화이트","베이직")
    clothes2_sizes = ("S","M","L","XL")
    gen_product("맨투맨2","누구나 소화 가능한 맨투맨",300,32000,clothes2_colors,clothes2_sizes,"상의","누나네옷가게",False)
    #clothes3
    clothes3_colors = ("블랙","화이트","그레이")
    clothes3_sizes = ("Free",)
    gen_product("반팔1","여름에 입으면 시원한 반팔",300,18000,clothes3_colors,clothes3_sizes,"상의","형아네옷가게",False)
    
    
    #clothes4
    clothes4_colors = ("블랙","화이트","그레이","레드","네이비")
    clothes4_sizes = ("Free",)
    gen_product("반팔2","인스타에서 핫한 반팔",200,13000,clothes4_colors,clothes4_sizes,"상의","이모네옷가게",False)
    
    #clothes5
    clothes5_colors = ("화이트","블루")
    clothes5_sizes = ("M","L")
    gen_product("셔츠1","핏이 좋은 셔츠",100,40000,clothes5_colors,clothes5_sizes,"상의","형아네옷가게",False)

    
    #clothes6
    clothes6_colors = ("블랙","화이트")
    clothes6_sizes = ("Free",)
    gen_product("셔츠2","오피스룩에 잘 어울리는 셔츠",200,45000,clothes6_colors,clothes6_sizes,"상의","누나네옷가게",False)
    
    #clothes7
    clothes7_colors = ("블랙","베이직")
    clothes7_sizes = ("27","28","29","30","31","32","33","34")
    gen_product("슬랙스1","기능성 좋은 슬랙스",200,28000,clothes7_colors,clothes7_sizes,"하의","형아네옷가게",False)
    
    
    #clothes8
    clothes8_colors = ("블랙","베이직")
    clothes8_sizes = ("27","28","29","30","31","32","33","34")
    gen_product("슬랙스2","연예인들이 많이 입는 슬랙스",200,25000,clothes8_colors,clothes8_sizes,"하의","형아네옷가게",False)
    
    #clothes9
    clothes9_colors = ("블랙")
    clothes9_sizes = ("26","27","28","29","30","31","32")
    gen_product("블랙진","무슨 옷을 입든 잘 어울리는 블랙진",200,30000,clothes9_colors,clothes9_sizes,"하의","누나네옷가게",False)

    
    #clothes10
    clothes10_colors = ("블루")
    clothes10_sizes = ("26","27","28","29","30","31","32")
    gen_product("청바지","여름에 입어도 시원한 청바지",200,23000,clothes10_colors,clothes10_sizes,"하의","이모네옷가게",False)

    
    #clothes11
    clothes11_colors = ("블랙","화이트","네이비")
    clothes11_sizes = ("Free",)
    gen_product("아우터1","겨울에 따뜻하게 입을 수 있는 롱코트",200,105000,clothes11_colors,clothes11_sizes,"아우터","누나네옷가게",False)

    
    #clothes12
    clothes12_colors = ("블랙","화이트","베이직")
    clothes12_sizes = ("Free",)
    gen_product("아우터2","가을에 너무 잘 어울리는 코트",200,77000,clothes12_colors,clothes12_sizes,"아우터","누나네옷가게",False)

    
    #clothes13
    clothes13_colors = ("베이직")
    clothes13_sizes = ("Free",)
    gen_product("아우터3","인스타 여신들이 입는 코트",200,90000,clothes13_colors,clothes13_sizes,"아우터","이모네옷가게",False)
    
    
    #clothes14
    clothes14_colors = ("블랙","베이직")
    clothes14_sizes = ("Free",)
    gen_product("아우터4","깔끔하게 입을 수 있는 블레이져",200,43000,clothes14_colors,clothes14_sizes,"아우터","누나네옷가게",False)
    
    
    #clothes15
    clothes15_colors = ("블랙","화이트")
    clothes15_sizes = ("235","240","245","250","255","260","265","270","275","280")
    gen_product("신발1","XX사에서 나온 깔끔한 디자인의 신발",200,89000,clothes15_colors,clothes15_sizes,"신발","형아네옷가게",False)
    
    
    #clothes16
    clothes16_colors = ("화이트")
    clothes16_sizes = ("235","240","245","250","255","260","265","270","275")
    gen_product("신발2","봄에 신으면 이쁜 신발",200,53000,clothes16_colors,clothes16_sizes,"신발","이모네옷가게",False)
    
    
    #clothes17
    clothes17_colors = ("블랙","화이트","네이비")
    clothes17_sizes = ("235","240","245","250","255","260","265","270","275")
    gen_product("신발3","모든 바지에 잘 어울리는 단화",200,63000,clothes17_colors,clothes17_sizes,"신발","누나네옷가게",False)
    
    
    #clothes18
    clothes18_colors = ("화이트","핑크","네이비")
    clothes18_sizes = ("Free")
    gen_product("치마1","인스타에서 핫한 치마",200,43000,clothes18_colors,clothes18_sizes,"원피스","누나네옷가게",False)
    
    
    
    
        