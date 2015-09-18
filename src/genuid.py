"""Generate a unique id.
"""
import base64
import uuid


def genuid():
    raw_bytes = uuid.uuid4().bytes
    b64_encoded = base64.urlsafe_b64encode(raw_bytes)
    return b64_encoded.rstrip("=")
