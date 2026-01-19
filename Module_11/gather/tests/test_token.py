from http import HTTPStatus


def test_get_details_success(
    client, mock_httpx_client_details, auth_headers
):
    response = client.get("/api/details/1", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "book" in data
    assert "reviews" in data
    assert data["book"]["id"] == 1
    assert data["book"]["title"] == "Test Book"
    assert len(data["reviews"]) == 1
    assert data["reviews"][0]["rating"] == 5
