def test_dashboards_get(test_client, init_database):
    response = test_client.get('/dashboards')
    assert response.status_code == 200
    assert response.json[0].get('admin') == 'Constantine'
    assert response.json[0].get('name') == 'Flask'
    assert response.json[0].get('id') == 55555

    response = test_client.get('/dashboards/12345')
    assert response.status_code == 404


def test_user_dashboards_get(test_client, init_database):
    response = test_client.get('/users/12345/dashboards')
    assert response.status_code == 200
    assert response.json[0].get('admin') == 'Constantine'
    assert response.json[0].get('name') == 'Flask'
    assert response.json[0].get('id') == 55555


def test_user_dashboards_post(test_client, init_database):
    response = test_client.get('/dashboards')
    assert response.status_code == 200
    assert response.json[0].get('admin') == 'Constantine'
    assert response.json[0].get('name') == 'Flask'
    assert response.json[0].get('id') == 55555

    response = test_client.post('/users/12345/dashboards',
                                json={"dashboard_name": "test"})
    assert response.status_code == 201
    assert isinstance(response.json.get('id'), int)

    response = test_client.post('/users/12345/dashboards',
                                json={"name": "test"})
    assert response.status_code == 400


def test_user_dashboards_detailed_post(test_client, init_database):
    response = test_client.post(f'/users/12345/dashboards/55555',
                                json={"team": "678910"})
    assert response.status_code == 201

    # not admin
    response = test_client.post(f'/users/11111/dashboards/55555',
                                json={"team": "678910"})
    assert response.status_code == 409

    # user does not exist
    response = test_client.post(f'/users/11111/dashboards/55555',
                                json={"team": "11111"})
    assert response.status_code == 400

    # dashboard does not exist
    response = test_client.post(f'/users/1234511/dashboards/11111',
                                json={"team": "678910"})
    assert response.status_code == 400


def test_user_dashboards_detailed_patch(test_client, init_database):
    response = test_client.patch(f'/users/12345/dashboards/55555',
                                 json={"dashboard_name": "new_test"})
    assert response.status_code == 204

    # not admin
    response = test_client.patch(f'/users/11111/dashboards/55555',
                                 json={"dashboard_name": "new_test"})
    assert response.status_code == 409

    # wrong input
    response = test_client.patch(f'/users/12345/dashboards/55555',
                                 json={"name": "new_name"})
    assert response.status_code == 400

    # wrong dashboard
    response = test_client.patch(f'/users/12345/dashboards/11111',
                                 json={"dashboard_name": "new_test"})
    assert response.status_code == 404


def test_user_dashboards_detailed_delete(test_client, init_database):
    response = test_client.delete(f'/users/678910/dashboards/55555')
    assert response.status_code == 409

    # wrong dashboard
    response = test_client.delete(f'/users/12345/dashboards/11111')
    assert response.status_code == 404

    response = test_client.delete(f'/users/12345/dashboards/55555')
    assert response.status_code == 200
