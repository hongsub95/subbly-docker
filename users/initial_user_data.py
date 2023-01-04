from . import models as User_models


def gen_user(apps, schema_editor):

    User_models.User.objects.create_superuser(username="admin", password="admin", name="관리자", email="", gender=User_models.User.GenderChoices.FEMALE)

    for id in range(2, 6):
        username = f"user{id}"
        password = f"user{id}"
        name = f"이름{id}"
        email = f"test{id}@test.com"
        login_method = User_models.User.login_method.LOGIN_EMAIL
        gender = User_models.User.gender.GENDER_MALE

        User_models.User.objects.create_user(username=username, password=password, name=name, email=email, gender=gender,login_method=login_method)

    User_models.User.objects.create_user(username="hong9506", password="payhere1", name="신홍섭", email="hong9056@gmail.com", gender=User_models.User.GenderChoices.MALE)