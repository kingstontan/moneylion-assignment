import pytest
from fastapi.testclient import TestClient

from app import crud, models
from app.database import Base, SessionLocal, engine, get_db
from app.main import app
from app.schemas import FeatureAccess, FeatureAccessRequest

client = TestClient(app)
db_session = SessionLocal()


@pytest.fixture()
def test_db():
    """util for creating tables before each test, then dropping them afterwards"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


""" CRUD utils """


def test_create_or_update_feature_access_entry_valid(test_db):
    result = crud.create_or_update_feature_access_entry(
        db_session,
        FeatureAccess(featureName="cool feature", email="abc@email.com", enable=True),
    )
    assert result == 200


def test_create_or_update_feature_access_entry_no_modified(test_db):
    result = crud.create_or_update_feature_access_entry(
        db_session,
        FeatureAccess(featureName="cool feature", email="abc@email.com", enable=True),
    )
    assert result == 200

    result = crud.create_or_update_feature_access_entry(
        db_session,
        FeatureAccess(featureName="cool feature", email="abc@email.com", enable=True),
    )
    assert result == 304


def test_get_feature_access_entry_empty(test_db):

    result = crud.get_feature_access_entry(
        db_session,
        FeatureAccessRequest(featureName="cool feature", email="abc@email.com"),
    )
    assert result is None


def test_get_feature_access_entry_valid(test_db):
    result = crud.create_or_update_feature_access_entry(
        db_session,
        FeatureAccess(featureName="cool feature", email="abc@email.com", enable=True),
    )
    assert result == 200

    result = crud.get_feature_access_entry(
        db_session,
        FeatureAccessRequest(featureName="cool feature", email="abc@email.com"),
    )
    assert type(result) is models.FeatureAccess
    assert result.enable is True


def test_get_feature_access_entry_update(test_db):
    # create entry
    result = crud.create_or_update_feature_access_entry(
        db_session,
        FeatureAccess(featureName="cool feature", email="abc@email.com", enable=True),
    )
    assert result == 200

    result = crud.get_feature_access_entry(
        db_session,
        FeatureAccessRequest(featureName="cool feature", email="abc@email.com"),
    )
    assert type(result) is models.FeatureAccess
    assert result.enable is True

    # update entry to enable=False
    result = crud.create_or_update_feature_access_entry(
        db_session,
        FeatureAccess(featureName="cool feature", email="abc@email.com", enable=False),
    )
    assert result == 200

    result = crud.get_feature_access_entry(
        db_session,
        FeatureAccessRequest(featureName="cool feature", email="abc@email.com"),
    )
    assert type(result) is models.FeatureAccess
    assert result.enable is False


""" Endpoints """


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "You have reached index ;)"}


def test_post_feature_valid(test_db):
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com", "enable": True},
    )
    assert response.status_code == 200


def test_post_feature_no_modified(test_db):
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com", "enable": True},
    )
    assert response.status_code == 200
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com", "enable": True},
    )
    assert response.status_code == 304


def test_post_feature_missing_param(test_db):
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com"},
    )
    assert response.status_code == 422
    response = client.post("/feature", json={})
    assert response.status_code == 422
    response = client.post("/feature")
    assert response.status_code == 422


def test_get_feature_valid(test_db):
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com", "enable": True},
    )
    assert response.status_code == 200
    response = client.get("/feature?email=abc@gmail.com&featureName=cool feature")
    assert response.status_code == 200
    assert response.json() == {"canAccess": True}


def test_updating_enable(test_db):
    # create entry
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com", "enable": True},
    )
    assert response.status_code == 200
    response = client.get("/feature?email=abc@gmail.com&featureName=cool feature")
    assert response.status_code == 200
    assert response.json() == {"canAccess": True}

    # update entry to enable=False
    response = client.post(
        "/feature",
        json={"featureName": "cool feature", "email": "abc@gmail.com", "enable": False},
    )
    assert response.status_code == 200
    response = client.get("/feature?email=abc@gmail.com&featureName=cool feature")
    assert response.status_code == 200
    assert response.json() == {"canAccess": False}


def test_get_feature_no_content(test_db):
    response = client.get("/feature?email=abc@gmail.com&featureName=cool feature")
    assert response.status_code == 204


def test_get_feature_missing_param(test_db):
    response = client.get("/feature?email=abc@gmail.com")
    assert response.status_code == 422
    response = client.get("/feature")
    assert response.status_code == 422
