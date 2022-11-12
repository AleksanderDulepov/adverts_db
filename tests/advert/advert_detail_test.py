import pytest

from advert.serializers import AdvertSerializer


@pytest.mark.django_db
def test_advert_detail_test(client, admin_token, advert):
    expected_response = AdvertSerializer(advert).data

    response = client.get(f"/adv/{advert.pk}/", HTTP_AUTHORIZATION="Bearer " + admin_token["token"])

    assert response.status_code == 200
    assert response.data == expected_response
