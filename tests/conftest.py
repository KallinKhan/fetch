import pytest
from run import initialize_app


@pytest.fixture
def client():
    app = initialize_app()

    with app.test_client() as client:
        yield client
