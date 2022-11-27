from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from . import crud, models
from .database import engine, get_db
from .schemas import FeatureAccess, FeatureAccessRequest, FeatureAccessResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def index():
    return {"message": "You have reached index ;)"}


@app.get("/feature", responses={200: {}, 204: {}}, response_model=FeatureAccessResponse)
def get_feature(
    email: str, featureName: str, response: Response, db: Session = Depends(get_db)
):
    entry: FeatureAccess = crud.get_feature_access_entry(
        db, FeatureAccessRequest(featureName=featureName, email=email)
    )

    if entry:
        response = FeatureAccessResponse(canAccess=entry.enable)
    else:
        # if there is no entry with the same composite pk(featureName & email)
        response.status_code = status.HTTP_204_NO_CONTENT
    return response


@app.post("/feature", responses={200: {}, 304: {}})
def post_feature(
    body: FeatureAccess, response: Response, db: Session = Depends(get_db)
):
    response.status_code = crud.create_or_update_feature_access_entry(
        db=db, feature_access=body
    )
    return response
