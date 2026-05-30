"""User profile persistence in Firestore."""

from datetime import datetime
from typing import Any, Dict, Optional

from auth.firebase import VALID_ROLES, get_firestore, init_firebase


def _users_collection():
    db = get_firestore()
    if db is None:
        return None
    return db.collection("users")


def get_user_profile(uid: str) -> Optional[Dict[str, Any]]:
    col = _users_collection()
    if col is None:
        return None
    doc = col.document(uid).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    data["uid"] = uid
    return data


def save_user_profile(uid: str, email: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    col = _users_collection()
    if col is None:
        raise RuntimeError("Firestore not available")

    existing = col.document(uid).get()
    base = existing.to_dict() if existing.exists else {}

    role = (payload.get("role") or base.get("role") or "student").lower()
    if role not in VALID_ROLES:
        role = "student"

    merged = {
        **base,
        **payload,
        "uid": uid,
        "email": email or base.get("email", ""),
        "role": role,
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    if not existing.exists:
        merged["created_at"] = merged["updated_at"]

    col.document(uid).set(merged, merge=True)
    return merged


def create_user_on_register(
    uid: str,
    email: str,
    role: str,
    display_name: str = "",
) -> Dict[str, Any]:
    if role not in VALID_ROLES:
        role = "student"

    profile = {
        "uid": uid,
        "email": email,
        "role": role,
        "display_name": display_name,
        "skills": [],
        "experiences": [],
        "internships": [],
        "resume_text": "",
        "project_descriptions": "",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }

    if init_firebase():
        save_user_profile(uid, email, profile)
    return profile
