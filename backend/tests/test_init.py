"""
General testing - proper app init & config.
"""


def test_app_factory(app):
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is True
    assert app.config['SECRET_KEY'] is not None
    assert app.config['ENV'] == 'testing'

