import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base  # Import Base from the correct location

class Shop(Base):
    """Database model for storing Shopify shop details and access tokens."""
    __tablename__ = "shops"
    # Explicitly set the schema for this table
    __table_args__ = {"schema": "app"}

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Shopify specific fields
    shop_domain: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
        comment="The unique *.myshopify.com domain for the shop."
    )
    access_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="The offline OAuth access token for the shop."
    )
    scopes: Mapped[str] = mapped_column(
        String,
        nullable=True, # Store as comma-separated string or consider a separate table
        comment="Access scopes granted during installation."
    )
    # Timestamps
    installed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp when the app was installed or token last updated."
    )
    uninstalled_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when the app was uninstalled (if applicable)."
    )

    # Potential future fields:
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # plan_name: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<Shop(id={self.id}, shop_domain='{self.shop_domain}')>" 