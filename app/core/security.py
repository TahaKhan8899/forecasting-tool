import hmac
import hashlib
import urllib.parse
import logging # Import logging
from typing import Dict, Any

logger = logging.getLogger(__name__) # Setup logger for this module

def verify_shopify_hmac(query_params: Dict[str, Any], shopify_secret: str) -> bool:
    """Verifies the HMAC signature of a request from Shopify.

    See: https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/authorization-code-grant#step-1-verify-the-installation-request

    Args:
        query_params: A dictionary representing the query parameters from the request.
        shopify_secret: The Shopify App's Client Secret.

    Returns:
        True if the HMAC is valid, False otherwise.
    """
    # Make a copy to avoid modifying the original dict
    params = query_params.copy()

    # Extract the received HMAC signature
    received_hmac = params.pop('hmac', None)
    if received_hmac is None:
        logger.warning("HMAC verification failed: 'hmac' parameter missing from query.")
        return False # Request is missing the HMAC parameter

    # Remove 'session' parameter if present (less common in OAuth flow, but good practice)
    params.pop('session', None)

    # The remaining parameters need to be sorted alphabetically by key
    sorted_keys = sorted(params.keys())
    # Rebuild the query string from sorted parameters
    message = "&".join([f"{key}={params[key]}" for key in sorted_keys])

    # --- BEGIN DEBUG LOGGING ---
    logger.debug(f"HMAC verification data:")
    logger.debug(f"  Received HMAC: {received_hmac}")
    logger.debug(f"  String to hash: '{message}'")
    # --- END DEBUG LOGGING ---

    # Calculate the HMAC digest using the app's secret key
    digest = hmac.new(
        shopify_secret.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    logger.debug(f"  Calculated digest: {digest}")

    # Compare the calculated digest with the received HMAC
    is_valid = hmac.compare_digest(digest, received_hmac)
    if not is_valid:
        logger.warning("HMAC verification failed: Calculated digest does not match received HMAC.")

    return is_valid 