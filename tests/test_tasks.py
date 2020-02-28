def test_tasks_get(test_client, init_database):
    response = test_client.get('/tasks/66666')
    assert response.status_code == 200
    assert response.json.get('admin_name') == 'Constantine'
    assert response.json.get('task_name') == 'Run tests'
    assert response.json.get('text') == 'Use Pytest'
    assert response.json.get('id') == 66666
    assert response.json.get('dashboard_id') == 55555


def test_user_tasks_get(test_client, init_database):

    response = test_client.get(f'/users/12345/dashboards/55555/tasks')
    assert response.status_code == 200
    assert not response.json


def test_user_tasks_post(test_client, init_database):
    response = test_client.post('/users/12345/dashboards/55555/tasks')
    assert response.status_code == 400

    response = test_client.post(f'/users/12345/dashboards/55555/tasks',
                                json={"task_name": "test",
                                      "text": "test"})
    assert response.status_code == 201
    assert isinstance(response.json.get('id'), int)

    # wrong input
    response = test_client.post(f'/users/12345/dashboards/55555/tasks',
                                json={"name": "test"})
    assert response.status_code == 400

    # not dashboard member
    response = test_client.post(f'/users/678910/dashboards/55555/tasks',
                                json={"task_name": "test",
                                      "text": "test"})
    assert response.status_code == 409

    # wrong dashboard
    response = test_client.post(f'/users/12345/dashboards/12345/tasks',
                                json={"task_name": "test",
                                      "text": "test"})
    assert response.status_code == 409


def test_user_tasks_detailed_post(test_client, init_database):
    response = test_client.post('/users/12345/dashboards/55555/tasks/66666')
    assert response.status_code == 400

    response = test_client.post('/users/12345/dashboards/55555/tasks/66666',
                                json={'team': 678910})
    assert response.status_code == 201

    # not dashboard member
    response = test_client.post('/users/678910/dashboards/55555/tasks/66666',
                                json={'team': 12345})
    assert response.status_code == 409

    # wrong dashboard
    response = test_client.post('/users/12345/dashboards/66666/tasks/66666',
                                json={'team': 678910})
    assert response.status_code == 409

    # task does not exist
    response = test_client.post('/users/12345/dashboards/55555/tasks/55555',
                                json={'team': 678910})
    assert response.status_code == 400


def test_user_tasks_detailed_patch(test_client, init_database):
    response = test_client.patch('/users/12345/dashboards/55555/tasks/66666',
                                 json={"task_name": "New task name"})
    assert response.status_code == 204

    # not dashboard member
    response = test_client.patch('/users/678910/dashboards/55555/tasks/66666',
                                 json={"task_name": "New task name"})
    assert response.status_code == 409

    # wrong input
    response = test_client.patch('/users/12345/dashboards/55555/tasks/66666',
                                 json={"name": "New task name"})
    assert response.status_code == 400

    # wrong dashboard
    response = test_client.patch('/users/12345/dashboards/1/tasks/66666',
                                 json={"task_name": "New task name"})
    assert response.status_code == 409

    # not admin changing admin
    # adding a new member to the dashboard
    response = test_client.patch('/users/54321/dashboards/55555/tasks/66666',
                                 json={"admin": 54321})
    assert response.status_code == 409
    assert b"Only task admins can change admins" in response.data


def test_user_task_detailed_delete(test_client, init_database):
    # wrong dashboard
    response = test_client.delete('/users/54321/dashboards/1/tasks/66666')
    assert response.status_code == 409

    # wrong task
    response = test_client.delete('/users/54321/dashboards/55555/tasks/1')
    assert response.status_code == 404

    # user not dashboard member
    response = test_client.delete('/users/678910/dashboards/55555/tasks/66666')
    assert response.status_code == 409

    response = test_client.delete('/users/12345/dashboards/55555/tasks/66666')
    assert response.status_code == 200
