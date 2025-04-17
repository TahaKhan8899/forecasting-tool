import secrets
import httpx
import logging
import re
from urllib.parse import urlencode
from typing import Tuple, Optional, Dict, Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import crud_shop
from app.models.shop import Shop

logger = logging.getLogger(__name__)

# Regex to validate shop domain format
SHOPIFY_DOMAIN_REGEX = re.compile(r"^[a-zA-Z0-9\-]+\.myshopify\.com$")

def generate_state_nonce() -> str:
    """Generates a secure random nonce for the OAuth state parameter."""
    return secrets.token_hex(16)

def build_shopify_auth_redirect_url(shop_domain: str, nonce: str) -> Tuple[str, str]:
    """Builds the Shopify OAuth authorization URL.

    Args:
        shop_domain: The target shop's domain.
        nonce: The unique state nonce for this request.

    Returns:
        A tuple containing the redirect URL and the nonce.
    Raises:
        HTTPException: If essential settings (API key, scopes, redirect URI) are missing.
    """
    if not settings.SHOPIFY_API_KEY or not settings.SHOPIFY_APP_SCOPES or not settings.SHOPIFY_REDIRECT_URI:
        logger.error("Shopify OAuth settings missing (API Key, Scopes, or Redirect URI)")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error for Shopify OAuth."
        )

    query_params = {
        "client_id": settings.SHOPIFY_API_KEY,
        "scope": settings.SHOPIFY_APP_SCOPES,
        "redirect_uri": settings.SHOPIFY_REDIRECT_URI,
        "state": nonce,
        "grant_options[]": "per-user" # Use 'per-user' for online tokens if needed, omit for offline (default)
        # If using offline tokens (recommended for most background access), remove 'grant_options[]'
    }
    # Remove grant_options if using offline tokens
    # For this example, we assume offline tokens are desired (most common for background tasks)
    del query_params["grant_options[]"] 

    redirect_url = f"https://{shop_domain}/admin/oauth/authorize?{urlencode(query_params)}"
    return redirect_url, nonce

async def exchange_code_for_token(shop_domain: str, code: str) -> Tuple[str, str]:
    """Exchanges the authorization code for an access token.

    Args:
        shop_domain: The shop's domain.
        code: The authorization code received from Shopify.

    Returns:
        A tuple containing the access token and the granted scopes.
    Raises:
        HTTPException: If the token exchange fails or returns invalid data.
    """
    token_url = f"https://{shop_domain}/admin/oauth/access_token"
    payload = {
        "client_id": settings.SHOPIFY_API_KEY,
        "client_secret": settings.SHOPIFY_API_SECRET,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(token_url, json=payload)
            response.raise_for_status() # Raise exception for 4xx or 5xx status codes
            data = response.json()
        except httpx.RequestError as exc:
            logger.error(f"HTTP Exception for {exc.request.url} - {exc}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail="Error communicating with Shopify API."
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP Status Error {exc.response.status_code} for {exc.request.url} - {exc.response.text}"
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail=f"Error obtaining token from Shopify: {exc.response.status_code}"
            )

    access_token = data.get("access_token")
    scopes = data.get("scope") # Note: 'scope' for offline, 'associated_user_scope' for online

    if not access_token or not scopes:
        logger.error(f"Invalid token response received from Shopify for {shop_domain}: {data}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to obtain valid access token from Shopify."
        )

    return access_token, scopes

async def process_shopify_callback(
    db: AsyncSession,
    shop_domain: str,
    code: str,
) -> None:
    """Handles the logic after Shopify redirects back to the app.

    1. Exchanges the code for an access token.
    2. Validates the returned scopes.
    3. Creates or updates the shop record in the database.

    Args:
        db: The SQLAlchemy AsyncSession.
        shop_domain: The shop's domain from the callback.
        code: The authorization code from the callback.

    Raises:
        HTTPException: If token exchange fails or DB operation fails.
    """
    # Step 4: Exchange code for token
    try:
        access_token, granted_scopes = await exchange_code_for_token(shop_domain, code)
    except HTTPException as e:
        # Re-raise the exception if token exchange fails
        raise e 

    # Optional Step: Confirm requested scopes (compare granted_scopes with settings.SHOPIFY_APP_SCOPES)
    requested_scopes_set = set(settings.SHOPIFY_APP_SCOPES.split(','))
    granted_scopes_set = set(granted_scopes.split(','))
    if not requested_scopes_set.issubset(granted_scopes_set):
        # Handle discrepancy - log, maybe raise error, or proceed with caution
        logger.warning(
            f"Shop {shop_domain} granted scopes '{granted_scopes}' which differ from requested '{settings.SHOPIFY_APP_SCOPES}'"
        )
        # Depending on app requirements, you might want to raise an exception here
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Required scopes not granted.")

    # Step 4 (cont.): Store the token and shop info
    try:
        db_shop = await crud_shop.get_shop_by_domain(db, shop_domain=shop_domain)
        if db_shop:
            logger.info(f"Updating existing shop record for {shop_domain}")
            await crud_shop.update_shop_token_and_scopes(
                db=db,
                db_shop=db_shop,
                access_token=access_token,
                scopes=granted_scopes
            )
        else:
            logger.info(f"Creating new shop record for {shop_domain}")
            await crud_shop.create_shop(
                db=db, 
                shop_domain=shop_domain, 
                access_token=access_token, 
                scopes=granted_scopes
            )
    except Exception as e:
        logger.error(f"Database error processing callback for {shop_domain}: {e}")
        # Consider more specific exception handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save installation details."
        )

def validate_shop_domain(shop: str) -> bool:
    """Validates the shop domain format."""
    if not shop or not isinstance(shop, str):
        return False
    return bool(SHOPIFY_DOMAIN_REGEX.match(shop)) 