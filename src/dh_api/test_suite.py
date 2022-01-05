def test_payloads_endpoints(client, example_payloads):
    for k, v in example_payloads.items():
        # correct request
        response = client.post(k, json=v)
        assert response.content_type == "application/json"
        assert response.status_code == 200

        # incorrect request
        assert client.post(k, json={"incorrect": "json"}).status_code == 400
        assert (
            client.post(
                k, data="incorrect request", content_type="multipart/form-data"
            ).status_code
            == 400
        )
