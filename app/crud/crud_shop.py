from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.shop import Shop

async def get_shop_by_domain(db: AsyncSession, *, shop_domain: str) -> Optional[Shop]:
    """Retrieves a shop record from the database based on its domain.

    Args:
        db: The SQLAlchemy AsyncSession.
        shop_domain: The shop's *.myshopify.com domain.

    Returns:
        The Shop object if found, otherwise None.
    """
    stmt = select(Shop).where(Shop.shop_domain == shop_domain)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_shop(
    db: AsyncSession,
    *, 
    shop_domain: str,
    access_token: str,
    scopes: Optional[str] = None
) -> Shop:
    """Creates a new shop record in the database.

    Args:
        db: The SQLAlchemy AsyncSession.
        shop_domain: The shop's *.myshopify.com domain.
        access_token: The obtained OAuth access token.
        scopes: The granted access scopes (comma-separated string).

    Returns:
        The newly created Shop object.
    """
    db_shop = Shop(
        shop_domain=shop_domain,
        access_token=access_token,
        scopes=scopes
        # installed_at is set by server_default
    )
    db.add(db_shop)
    await db.commit()
    await db.refresh(db_shop)
    return db_shop

async def update_shop_token_and_scopes(
    db: AsyncSession,
    *,
    db_shop: Shop, 
    access_token: str,
    scopes: Optional[str] = None
) -> Shop:
    """Updates an existing shop's access token and scopes.

    Also resets uninstalled_at if it was previously set.

    Args:
        db: The SQLAlchemy AsyncSession.
        db_shop: The existing Shop object to update.
        access_token: The new OAuth access token.
        scopes: The new granted access scopes (comma-separated string).

    Returns:
        The updated Shop object.
    """
    update_data = {
        "access_token": access_token,
        "scopes": scopes,
        "uninstalled_at": None # Reset uninstall timestamp on reinstall/update
    }
    stmt = update(Shop).where(Shop.id == db_shop.id).values(**update_data)
    await db.execute(stmt)
    await db.commit()
    await db.refresh(db_shop) # Refresh to get updated data
    return db_shop

async def mark_shop_uninstalled(db: AsyncSession, *, db_shop: Shop) -> Shop:
    """Marks a shop as uninstalled by setting the uninstalled_at timestamp.

    Args:
        db: The SQLAlchemy AsyncSession.
        db_shop: The Shop object to mark as uninstalled.

    Returns:
        The updated Shop object.
    """
    # Optionally, you might want to clear the access token as well
    # db_shop.access_token = ""
    db_shop.uninstalled_at = func.now() # Use func.now() if not automatically handled by ORM/DB
    # Or assign datetime.datetime.now(datetime.timezone.utc)
    await db.commit()
    await db.refresh(db_shop)
    return db_shop 