import pytest

from commands import create_db, delete_db, seed_db
from main import create_app


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    with app.app_context():
        delete_db()
        create_db()
        seed_db()
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
