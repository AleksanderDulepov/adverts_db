import json

import pytest
from django.forms import model_to_dict

from advert.serializers import AdvertSerializer


@pytest.mark.django_db
def test_advert_create_by_url(client, advert):
    expected_response = {"name": "this_is_test_name",
                         "price": 1,
                         "description": "test_description",
                         "is_published": False,
                         "image": None,
                         "author": advert.author.id,
                         "category": advert.category.id
                         }

    data = model_to_dict(advert, exclude=["image"])

    response = client.post("/adv/create/",
                           data,
                           content_type="application/json",
                           )


    del response.data["id"]

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_advert_create_by_fixture(client, advert, admin_token):
    expected_response = AdvertSerializer(advert).data

    response = client.get(f"/adv/{advert.pk}/", HTTP_AUTHORIZATION="Bearer " + admin_token["token"])

    assert response.status_code == 200
    assert json.loads(response.content) == expected_response
