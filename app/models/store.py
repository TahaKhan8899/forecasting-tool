from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Index
from sqlalchemy.sql import expression

from app.db.session import Base


class Store(Base):
    """SQLAlchemy model for storing Shopify store connection details."""
    
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_url = Column(String, unique=True, nullable=False, index=True)
    access_token = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=expression.true(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Table arguments including schema and index
    __table_args__ = (
        Index("ix_stores_store_url", "store_url"),
        {"schema": "app"}
    )
    
    def __repr__(self) -> str:
        return f"<Store(id={self.id}, store_url='{self.store_url}', is_active={self.is_active})>" 