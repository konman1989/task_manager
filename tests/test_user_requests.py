def test_users_get(test_client, init_database):
    response = test_client.get('/users')

    assert response.status_code == 200
    assert b'Constantine' in response.data
    assert b'Steve' in response.data
    assert b'steve@gmail.com' in response.data

    response = test_client.get('/users/12345')
    assert response.status_code == 200
    assert response.json.get('email') == 'constantine@gmail.com'
    assert response.json.get('chat_id') == 12345


def test_users_post(test_client, init_database):
    response = test_client.post('/users')
    assert response.status_code == 400

    response = test_client.post('/users', json={"chat_id": 11111,
                                                "username": "Bob",
                                                "email": "bob@gmail.com"}
                                )
    assert response.status_code == 201

    response = test_client.post('/users', json={"id": 50000, "user": "Steve"})
    assert response.status_code == 400


def test_users_patch(test_client, init_database):
    response = test_client.patch('/users/678910', json={"username": "Bob"})
    assert response.status_code == 204

    response = test_client.get('/users/678910')
    assert response.json.get('username') == 'Bob'

    response = test_client.patch('/users/678910', json={"skype": "Bob_skype"})
    assert response.status_code == 400


def test_users_delete(test_client, init_database):
    response = test_client.delete('/users/12345')
    assert response.status_code == 200

    test_client.post('/users', json={"chat_id": 55555,
                                     "username": "Tom",
                                     "email": "tom@gmail.com"}
                     )
    response = test_client.delete('/users/55555')
    assert response.status_code == 200
