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


@app.post("/feature")
def post_feature(
    body: FeatureAccess, response: Response, db: Session = Depends(get_db)
):
    response.status_code = crud.create_or_update_feature_access_entry(
        db=db, feature_access=body
    )

    return response
