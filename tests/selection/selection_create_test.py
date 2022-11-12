import pytest
from django.forms import model_to_dict

from advert.serializers import AdvertSerializer, AdvertCreateSerializer
from selection.serializers import SelectionCreateSerializer
from tests.factories import AdvertFactory


@pytest.mark.django_db
def test_selection_create_single(client, admin_token, advert):

    data = {
        "name":"test_selection_name",
        "items":[advert.id]
    }

    expected_response = {"name": "test_selection_name",
                         "owner":admin_token["id_from_token"],
                         "items":[advert.id]
                         }

    response = client.post("/selection/",
                           data,
                           content_type="application/json",
                           HTTP_AUTHORIZATION="Bearer " + admin_token["token"])

    del response.data["id"]

    assert response.status_code == 201
    assert response.data == expected_response

@pytest.mark.django_db
def test_selection_create(client, admin_token):
    adverts=AdvertFactory.create_batch(2)

    data = {
        "name":"test_selection_name",
        "items":[advert.id for advert in adverts]
    }

    expected_response = {"name": "test_selection_name",
                         "owner": admin_token["id_from_token"],
                         "items":[advert.id for advert in adverts],
                         }

    response = client.post("/selection/",
                           data,
                           content_type="application/json",
                           HTTP_AUTHORIZATION="Bearer " + admin_token["token"])

    del response.data["id"]

    assert response.status_code == 201
    assert response.data == expected_response