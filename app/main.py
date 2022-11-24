from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from app.schemas import FeatureAccess, FeatureAccessRequest, FeatureAccessResponse

from . import crud, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/feature", response_model=FeatureAccessResponse)
def get_feature(email: str, featureName: str, db: Session = Depends(get_db)):
    entry: FeatureAccess = crud.get_feature_access_entry(
        db, FeatureAccessRequest(featureName=featureName, email=email)
    )

    response = FeatureAccessResponse(canAccess=entry.enable)
    return response


def set_feature_access(request: FeatureAccess):
    if 0 == 0:
        return status.HTTP_200_OK
    else:
        return status.HTTP_304_NOT_MODIFIED


@app.post("/feature")
def post_feature(
    body: FeatureAccess, response: Response, db: Session = Depends(get_db)
):

    crud.create_feature_access_entry(db=db, feature_access=body)
    response.status_code = set_feature_access(body)

    return response
