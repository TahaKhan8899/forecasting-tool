from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class StoreBase(BaseModel):
    """Base Pydantic schema for Shopify store data."""
    
    store_url: str = Field(..., description="Shopify store URL (e.g., 'store-name.myshopify.com')")
    is_active: bool = Field(True, description="Whether the store connection is active")


class StoreCreate(StoreBase):
    """Schema for creating a new Shopify store connection."""
    
    access_token: str = Field(..., description="OAuth access token for the Shopify store")


class StoreUpdate(BaseModel):
    """Schema for updating an existing Shopify store connection."""
    
    store_url: Optional[str] = Field(None, description="Shopify store URL")
    access_token: Optional[str] = Field(None, description="OAuth access token for the Shopify store")
    is_active: Optional[bool] = Field(None, description="Whether the store connection is active")


class StoreRead(StoreBase):
    """Schema for reading Shopify store data (excludes sensitive fields)."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class Store(StoreRead):
    """Full Shopify store schema with access token (for internal use only)."""
    
    access_token: str
    
    class Config:
        orm_mode = True 