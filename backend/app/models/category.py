import uuid

from sqlalchemy import Boolean, Column, DateTime, String, Text, Uuid, func
from sqlalchemy.orm import relationship

from app.configs.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name = Column(String(150), nullable=False)
    slug = Column(String(180), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    subcategories = relationship(
        "SubCategory",
        back_populates="category",
        cascade="all, delete-orphan",
    )
    products = relationship("Product", back_populates="category")