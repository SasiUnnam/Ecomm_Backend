from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.configs.database import Base
from app.models.product import Product  # noqa: F401
from app.models.user import User  # noqa: F401


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    shipping_address_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("addresses.id") if "addresses" in Base.metadata.tables else None,
        nullable=True,
        index=True,
    )
    billing_address_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("addresses.id") if "addresses" in Base.metadata.tables else None,
        nullable=True,
        index=True,
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )
    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )
    shipping_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    payment_status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    placed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.id"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(100), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
