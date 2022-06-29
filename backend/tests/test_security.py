"""
Security-related testing - JWT configuration and responses.
"""
import json


def test_login_correct_credentials(app, client):
    """
    Given a populated test DB.
    When POST /login body contains correct login credentials.
    Then REST endpoint returns auth token & refresh token with status 200.
    """
    response = client.post('/login', data=json.dumps({
        'username': 'testuse2r',
        'password': 'password'
    }), headers={'Content-Type': 'application/json'})
    print(response.request.data)
    assert response.status_code == 200
