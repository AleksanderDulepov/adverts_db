import pytest


@pytest.fixture
@pytest.mark.django_db
def admin_token(client, django_user_model):

    username = "test_auth_username"
    password = "test_password"
    birth_date = "2010-10-10"
    email = "test1@mail.ru"
    is_superuser = True

    user=django_user_model.objects.create_user(username=username, password=password, birth_date=birth_date, email=email,
                                          is_superuser=is_superuser)

    response = client.post("/user/login/",
                           {"username": username, "password": password},
                           content_type="application/json",)

    return {"token":response.data["access"],"id_from_token":user.pk}