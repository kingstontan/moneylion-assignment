from sqlalchemy import Boolean, Column, Index, String

from .database import Base


class FeatureAccess(Base):
    __tablename__ = "feature_access"

    featureName = Column(String, primary_key=True)
    email = Column(String, primary_key=True)
    enable = Column(Boolean, default=True)

    # TODO: properly define index
    # __table_args__ = (
    #     Index(
    #         "user_permission",
    #         "featureName",
    #         "email",
    #     ),
    # )
