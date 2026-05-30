"""Firebase Admin initialization and token verification."""

import json
import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_firebase_app = None
_firestore_client = None


def is_firebase_client_configured() -> bool:
    """True when the web client has enough config (API key + project)."""
    config = get_public_firebase_config()
    return bool(config.get("apiKey") and config.get("projectId"))


def is_firebase_admin_configured() -> bool:
    """Return True when enough config exists to initialize Firebase Admin."""
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if cred_path:
        from pathlib import Path

        if Path(cred_path).is_file():
            return True
    if os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"):
        return True
    if os.getenv("FIREBASE_PROJECT_ID") and os.getenv("FIREBASE_PRIVATE_KEY"):
        return True
    return False


def is_firebase_configured() -> bool:
    """Alias for admin SDK availability."""
    return is_firebase_admin_configured()


def get_public_firebase_config() -> Dict[str, str]:
    """Web client Firebase config (public keys only)."""
    return {
        "apiKey": os.getenv("FIREBASE_API_KEY", ""),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.getenv("FIREBASE_APP_ID", ""),
    }


def init_firebase() -> bool:
    """Initialize Firebase Admin SDK. Returns True on success."""
    global _firebase_app, _firestore_client

    if _firebase_app is not None:
        return True

    if not is_firebase_configured():
        logger.warning("Firebase not configured — auth endpoints will be limited.")
        return False

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if firebase_admin._apps:
            _firebase_app = firebase_admin.get_app()
        else:
            cred = None
            sa_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            if sa_json:
                cred = credentials.Certificate(json.loads(sa_json))
            elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
            elif os.getenv("FIREBASE_PROJECT_ID"):
                cred = credentials.Certificate(
                    {
                        "type": "service_account",
                        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
                        "private_key": (
                            os.getenv("FIREBASE_PRIVATE_KEY", "")
                            .replace("\\n", "\n")
                        ),
                        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
                        "client_id": os.getenv("FIREBASE_CLIENT_ID", ""),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                )
            if cred is None:
                return False
            _firebase_app = firebase_admin.initialize_app(cred)

        _firestore_client = firestore.client()
        logger.info("Firebase Admin initialized")
        return True
    except Exception as exc:
        logger.error("Firebase init failed: %s", exc)
        return False


def get_firestore():
    """Return Firestore client or None."""
    if _firestore_client is None:
        init_firebase()
    return _firestore_client


def verify_id_token(id_token: str) -> Optional[Dict[str, Any]]:
    """Verify Firebase ID token; return decoded claims or None."""
    if not id_token:
        return None
    if not init_firebase():
        return None
    try:
        from firebase_admin import auth

        return auth.verify_id_token(id_token)
    except Exception as exc:
        logger.warning("Token verification failed: %s", exc)
        return None


def set_user_role(uid: str, role: str) -> bool:
    """Set Firebase custom claim for RBAC."""
    if not init_firebase():
        return False
    try:
        from firebase_admin import auth

        auth.set_custom_user_claims(uid, {"role": role})
        return True
    except Exception as exc:
        logger.error("Failed to set role claim: %s", exc)
        return False


VALID_ROLES = frozenset({"student", "recruiter", "admin"})
