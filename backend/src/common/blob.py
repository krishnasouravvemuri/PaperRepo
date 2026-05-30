"""Supabase Storage client. Uploads file bytes, returns signed URLs.

DB keeps only the object path; bytes live in the Supabase bucket.
"""

from django.conf import settings
from supabase import Client, create_client


class BlobClient:
    _client: Client | None = None

    @classmethod
    def _get(cls) -> Client:
        if cls._client is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
                raise RuntimeError("SUPABASE_URL / SUPABASE_SERVICE_KEY not configured.")
            cls._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        return cls._client

    @classmethod
    def upload(cls, path: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        bucket = cls._get().storage.from_(settings.SUPABASE_BUCKET)
        bucket.upload(
            path=path,
            file=content,
            file_options={"content-type": content_type, "upsert": "false"},
        )
        return path

    @classmethod
    def signed_url(cls, path: str, ttl: int | None = None) -> str:
        ttl = ttl or settings.SUPABASE_SIGNED_URL_TTL
        bucket = cls._get().storage.from_(settings.SUPABASE_BUCKET)
        res = bucket.create_signed_url(path, ttl)
        return res.get("signedURL") or res.get("signedUrl") or ""

    @classmethod
    def delete(cls, path: str) -> None:
        bucket = cls._get().storage.from_(settings.SUPABASE_BUCKET)
        bucket.remove([path])
