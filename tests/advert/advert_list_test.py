import json

import pytest

from advert.serializers import AdvertSerializer
from tests.factories import AdvertFactory


@pytest.mark.django_db
def test_advert_list(client):
    items_amount=10
    adverts = AdvertFactory.create_batch(items_amount)

    expected_response = {
        "count": items_amount,
        "next": None,
        "previous": None,
        "results": AdvertSerializer(adverts, many=True).data,
    }

    response = client.get("/adv/")

    assert response.status_code == 200
    assert json.loads(response.content) == expected_response

