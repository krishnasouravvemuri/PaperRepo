"""Storage path builder. DB stores these paths only; never the file bytes."""

import os
import uuid


class BlobPaths:
    """
    Layout in the Supabase Storage bucket:
        {user_id}/question_papers/{uuid}{ext}
        {user_id}/important_topics/{uuid}{ext}
        {user_id}/materials/{uuid}{ext}
    """

    @staticmethod
    def _build(user_id: str, category: str, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        return f"{user_id}/{category}/{uuid.uuid4().hex}{ext}"

    @classmethod
    def question_paper(cls, user_id: str, filename: str) -> str:
        return cls._build(user_id, "question_papers", filename)

    @classmethod
    def important_topic(cls, user_id: str, filename: str) -> str:
        return cls._build(user_id, "important_topics", filename)

    @classmethod
    def material(cls, user_id: str, filename: str) -> str:
        return cls._build(user_id, "materials", filename)
