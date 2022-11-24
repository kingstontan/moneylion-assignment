from fastapi import status
from sqlalchemy.orm import Session

from app.schemas import FeatureAccess, FeatureAccessRequest

from . import models


def get_feature_access_entry(
    db: Session, request: FeatureAccessRequest
) -> models.FeatureAccess:

    return (
        db.query(models.FeatureAccess)
        .filter(models.FeatureAccess.featureName == request.featureName)
        .filter(models.FeatureAccess.email == request.email)
    ).first()


def create_or_update_feature_access_entry(
    db: Session, feature_access: FeatureAccess
) -> status:
    response_status = status.HTTP_200_OK
    feature_access_request = FeatureAccessRequest(
        featureName=feature_access.featureName, email=feature_access.email
    )
    if feature_access_entry := get_feature_access_entry(db, feature_access_request):
        if feature_access_entry.enable == feature_access.enable:
            response_status = status.HTTP_304_NOT_MODIFIED
        else:
            feature_access_entry.enable = feature_access.enable
    else:
        feature_access_entry = models.FeatureAccess(**feature_access.dict())
        db.add(feature_access_entry)

    db.commit()
    db.refresh(feature_access_entry)
    return response_status
