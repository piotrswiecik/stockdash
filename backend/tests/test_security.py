"""
Security-related testing - JWT configuration and responses.
Recommended to independently test endpoints with Postman.
"""


def test_login_correct_credentials(app, client):
    """
    Given a populated test DB.
    When POST /login body contains correct login credentials.
    Then REST endpoint returns auth token & refresh token with status 200.
    """
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json
    assert response.json['access_token'] != ''
    assert response.json['refresh_token'] != ''


def test_login_incorrect_username(app, client):
    """
    Given a populated test DB.
    When POST /login body contains incorrect username (non-existent user).
    Then REST endpoint returns 401 with error message.
    :param app:
    :param client:
    :return:
    """
    response = client.post('/login', json={
        'username': 'boromir',
        'password': 'password'
    })
    assert response.status_code == 401
    assert 'access_token' not in response.json
    assert 'refresh_token' not in response.json
    assert 'message' in response.json
    assert response.json['message'] == 'Authorization failed'


def test_login_incorrect_password(app, client):
    """
    Given a populated test DB.
    When POST /login body contains incorrect password for existing user.
    Then REST endpoint returns 401 with error message.
    """
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'thiswontwork'
    })
    assert response.status_code == 401
    assert 'access_token' not in response.json
    assert 'refresh_token' not in response.json
    assert 'message' in response.json
    assert response.json['message'] == 'Authorization failed'
