from pydantic import BaseModel


class FeatureAccessRequest(BaseModel):
    featureName: str
    email: str

    class Config:
        orm_mode = True


class FeatureAccessResponse(BaseModel):
    canAccess: bool

    class Config:
        orm_mode = True


class FeatureAccess(BaseModel):
    featureName: str
    email: str
    enable: bool

    class Config:
        orm_mode = True
