from fastapi import status
from sqlalchemy.orm import Session

from app.schemas import FeatureAccess, FeatureAccessRequest

from . import models


def get_feature_access_entry(
    db: Session, request: FeatureAccessRequest
) -> models.FeatureAccess:
    """Query the DB for a FeatureAccess entry

    Args:
        request: a FeatureAccessRequest containing featureName & email

    Returns:
        A FeatureAccess entry if the query exists; else returns None
    """

    return (
        db.query(models.FeatureAccess)
        .filter(models.FeatureAccess.featureName == request.featureName)
        .filter(models.FeatureAccess.email == request.email)
    ).first()


def create_or_update_feature_access_entry(
    db: Session, feature_access: FeatureAccess
) -> status:
    """Upsert a FeatureAccess entry.
    Query for an entry with the same featureName & email (composite pk)

    Args:
        request: a FeatureAccess containing featureName, email & enable

    Returns:
        A HTTP status, HTTP_200_OK if a new entry was created;
        HTTP_304_NOT_MODIFIED if nothing was modified
    """
    response_status = status.HTTP_200_OK
    feature_access_request = FeatureAccessRequest(
        featureName=feature_access.featureName, email=feature_access.email
    )

    if existing_entry := get_feature_access_entry(db, feature_access_request):
        if existing_entry.enable == feature_access.enable:
            response_status = status.HTTP_304_NOT_MODIFIED
        else:
            existing_entry.enable = feature_access.enable
    else:
        new_entry = models.FeatureAccess(**feature_access.dict())
        db.add(new_entry)
    db.commit()

    return response_status
