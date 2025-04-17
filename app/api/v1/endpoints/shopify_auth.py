import logging
import secrets
from typing import Optional, Dict, Any

from fastapi import APIRouter, Request, Response, Depends, Query, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_shopify_hmac
from app.services import (
    generate_state_nonce,
    build_shopify_auth_redirect_url,
    process_shopify_callback,
    validate_shop_domain
)
from app.api.deps import get_db # Use the existing dependency function name: get_db

logger = logging.getLogger(__name__)

router = APIRouter()

# State cookie details
STATE_COOKIE_NAME = "shopify_oauth_state"
# Set cookie expiry significantly shorter than nonce validity if needed,
# but usually matching nonce lifetime or session lifetime is fine.
STATE_COOKIE_MAX_AGE_SECONDS = 600 # 10 minutes

@router.get("/install", summary="Initiate Shopify OAuth Installation")
async def shopify_install(request: Request,
                          shop: str = Query(..., description="The shop domain (*.myshopify.com)")
                          ) -> RedirectResponse:
    """
    Handles the initial app installation request from Shopify or the merchant.

    - Validates the shop domain format.
    - Generates a state nonce for security.
    - Builds the Shopify authorization URL.
    - Stores the nonce in a signed HTTPOnly cookie.
    - Redirects the user to the Shopify authorization URL.
    """
    logger.info(f"Received install request for shop: {shop}")

    # Basic validation of the shop parameter
    if not validate_shop_domain(shop):
        logger.warning(f"Invalid shop domain format received: {shop}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid shop domain format.")

    # Step 2: Request authorization code
    nonce = generate_state_nonce()
    try:
        redirect_url, _ = build_shopify_auth_redirect_url(shop_domain=shop, nonce=nonce)
    except HTTPException as e:
        # Propagate exceptions from service layer (e.g., config errors)
        raise e

    response = RedirectResponse(url=redirect_url)
    
    # Set the state nonce in a secure, signed cookie
    # The actual signing happens via SessionMiddleware based on request.session
    request.session[STATE_COOKIE_NAME] = nonce
    logger.info(f"Redirecting shop {shop} to Shopify for authorization.")
    return response


@router.get("/callback", summary="Handle Shopify OAuth Callback")
async def shopify_callback(
    request: Request,
    response: Response, # Response object is automatically available, no need to pass explicitly
    db: AsyncSession = Depends(get_db), # Corrected dependency function
    # Shopify sends these parameters back
    code: Optional[str] = Query(None),
    hmac: Optional[str] = Query(None),
    host: Optional[str] = Query(None), # Base64 encoded admin host
    shop: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    timestamp: Optional[str] = Query(None),
) -> RedirectResponse:
    """
    Handles the redirect back from Shopify after the user authorizes the app.

    - Validates the received state against the value stored in the session cookie.
    - Verifies the HMAC signature of the request.
    - Validates the shop domain format.
    - Exchanges the authorization code for an access token using the service layer.
    - Stores the access token securely (handled by the service layer -> CRUD).
    - Redirects the user to the app's UI.
    """
    logger.info(f"Received callback for shop: {shop}")

    # Retrieve state from signed session cookie
    stored_state = request.session.pop(STATE_COOKIE_NAME, None)

    # Step 3: Validate authorization code
    # 3.1: Check state parameter
    if stored_state is None or state is None or not secrets.compare_digest(stored_state, state):
        logger.error(f"State mismatch for shop {shop}. Received: '{state}', Expected: '{stored_state}'")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid state parameter.")

    # 3.2: Check HMAC signature
    if hmac is None or shop is None or timestamp is None or code is None:
         logger.error(f"Missing required parameters in callback for shop {shop}")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required callback parameters.")

    # Get all query params for HMAC verification
    query_params = dict(request.query_params)
    if not verify_shopify_hmac(query_params=query_params, shopify_secret=settings.SHOPIFY_API_SECRET):
        logger.error(f"HMAC verification failed for shop {shop}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid HMAC signature.")

    # 3.3: Validate shop domain format again
    if not validate_shop_domain(shop):
        logger.warning(f"Invalid shop domain format received in callback: {shop}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid shop domain format in callback.")

    # If all checks pass, proceed to exchange code and store token
    logger.info(f"Callback validation successful for shop: {shop}. Exchanging code.")
    try:
        await process_shopify_callback(db=db, shop_domain=shop, code=code)
    except HTTPException as e:
        # Handle errors during code exchange or DB operations
        logger.error(f"Error processing callback for shop {shop}: {e.detail}")
        raise e # Re-raise the exception to return appropriate HTTP error
    
    # Step 5: Redirect to App UI
    # Clear the state cookie explicitly if it wasn't popped or if using regular cookies
    # response.delete_cookie(STATE_COOKIE_NAME, httponly=True, samesite="lax", secure=request.url.scheme == "https")
    # Redirect to your app's frontend, potentially passing shop or host 
    # The exact URL depends on your frontend routing
    app_dashboard_url = f"/dashboard?shop={shop}" # Example redirect URL
    if host: 
         app_dashboard_url += f"&host={host}" # Pass host if needed by embedded apps (though this is non-embedded)
    
    logger.info(f"Successfully processed callback for shop {shop}. Redirecting to dashboard.")
    return RedirectResponse(url=app_dashboard_url) 