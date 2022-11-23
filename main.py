from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class FeatureAccessResponse(BaseModel):
    canAccess: bool


def can_access(email: str, featureName: str) -> FeatureAccessResponse:
    response = FeatureAccessResponse(canAccess=True)
    return response


@app.get("/feature", response_model=FeatureAccessResponse)
async def get_feature(email: str, featureName: str):
    response = can_access(email, featureName)
    return response


class FeatureAccess(BaseModel):
    featureName: str
    email: str
    enable: bool


def set_feature_access(request: FeatureAccess) -> status:
    if 0 == 0:
        return status.HTTP_200_OK
    else:
        return status.HTTP_304_NOT_MODIFIED


@app.post("/feature")
async def post_feature(body: FeatureAccess, response: Response):
    response.status_code = set_feature_access(body)

    return response
