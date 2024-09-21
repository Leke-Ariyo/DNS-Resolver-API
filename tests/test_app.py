import pytest
from app import create_app


@pytest.fixture
def client():
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }

    app = create_app(config)  # Pass the custom configuration
    with app.test_client() as client:
        with app.app_context():
            # Create the database schema for testing
            from app import db
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_home(client):
    """Test the home endpoint returns correct data"""
    rv = client.get('/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "version" in json_data
    assert "date" in json_data
    assert "kubernetes" in json_data
