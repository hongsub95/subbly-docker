from . import models as User_models


def gen_users(apps, schema_editor):

    User_models.User.objects.create_superuser(username="admin@admin.com", password="admin", name="관리자",  gender=User_models.User.GenderChoices.FEMALE)

    for id in range(2, 6):
        password = f"user{id}"
        name = f"이름{id}"
        username = f"test{id}@test.com"
        login_method = User_models.User.LoginChoices.EMAIL
        gender = User_models.User.GenderChoices.MALE

        User_models.User.objects.create_user(username=username, password=password, name=name,  gender=gender,login_method=login_method)

    User_models.User.objects.create_user(username="hong9506@gmail.com", password="hong9506", name="신홍섭", gender=User_models.User.GenderChoices.MALE)