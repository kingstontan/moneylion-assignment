from sqlalchemy.orm import Session

from . import models, schemas


def get_feature_access_entry(
    db: Session, request: schemas.FeatureAccessRequest
) -> models.FeatureAccess:

    return (
        db.query(models.FeatureAccess)
        .filter(models.FeatureAccess.featureName == request.featureName)
        .filter(models.FeatureAccess.email == request.email)
    ).first()


def create_feature_access_entry(db: Session, feature_access: schemas.FeatureAccess):
    feature_access_entry = models.FeatureAccess(**feature_access.dict())
    db.add(feature_access_entry)
    db.commit()
    db.refresh(feature_access_entry)
    return feature_access_entry
