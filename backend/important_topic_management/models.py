"""Important topic business logic. ORM models live in core.client_model_app."""

from django.utils import timezone

from core.client_model_app.models import Faculties, ImportantTopics
from src.common.blob import BlobClient
from src.common.blob_paths import BlobPaths
from subject_management.models import SubjectManagement


def _get_faculty(faculty_name: str | None) -> Faculties | None:
    name = (faculty_name or "").strip()
    if not name:
        return None
    faculty, _ = Faculties.objects.get_or_create(faculty_name=name)
    return faculty


def _serialize(t: ImportantTopics) -> dict:
    return {
        "important_topic_id": str(t.important_topic_id),
        "important_topic_title": t.important_topic_title,
        "subject_code": t.fk_subject.subject_code,
        "subject_name": t.fk_subject.subject_name,
        "important_topic_exam_type": t.important_topic_exam_type,
        "faculty_name": t.fk_faculty.faculty_name if t.fk_faculty else "",
        "uploaded_by": t.fk_user.user_name,
    }


class ImportantTopicManagement:
    @staticmethod
    def create(user_id: str, payload: dict, files: list) -> tuple[int, str, dict | None]:
        subject = SubjectManagement.get_or_create(payload["subject_code"], payload["subject_name"])
        faculty = _get_faculty(payload.get("faculty_name"))
        created = []
        for f in files:
            path = BlobPaths.important_topic(user_id, f.name)
            BlobClient.upload(path, f.read(), getattr(f, "content_type", "application/octet-stream"))
            topic = ImportantTopics.objects.create(
                fk_user_id=user_id,
                fk_subject=subject,
                fk_faculty=faculty,
                important_topic_title=payload["important_topic_title"],
                important_topic_exam_type=payload["important_topic_exam_type"],
                important_topic_file_path=path,
            )
            created.append(str(topic.important_topic_id))
        return 201, f"{len(created)} file(s) uploaded.", {"created_ids": created}

    @staticmethod
    def list_topics(filters: dict) -> tuple[int, str, list]:
        qs = (
            ImportantTopics.objects.filter(important_topic_deleted_at__isnull=True)
            .select_related("fk_subject", "fk_user", "fk_faculty")
            .order_by("-important_topic_created_at")
        )
        if filters.get("course_code"):
            qs = qs.filter(fk_subject__subject_code__icontains=filters["course_code"].strip().upper())
        if filters.get("exam_type"):
            qs = qs.filter(important_topic_exam_type=filters["exam_type"])
        return 200, "OK", [_serialize(t) for t in qs]

    @staticmethod
    def list_mine(user_id: str) -> tuple[int, str, list]:
        qs = (
            ImportantTopics.objects.filter(fk_user_id=user_id, important_topic_deleted_at__isnull=True)
            .select_related("fk_subject", "fk_user", "fk_faculty")
            .order_by("-important_topic_created_at")
        )
        return 200, "OK", [_serialize(t) for t in qs]

    @staticmethod
    def get_file_url(topic_id: str) -> tuple[int, str, dict | None]:
        topic = ImportantTopics.objects.filter(
            important_topic_id=topic_id, important_topic_deleted_at__isnull=True
        ).first()
        if not topic:
            return 404, "Not found.", None
        return 200, "OK", {"url": BlobClient.signed_url(topic.important_topic_file_path)}

    @staticmethod
    def update(user_id: str, topic_id: str, payload: dict) -> tuple[int, str, dict | None]:
        topic = ImportantTopics.objects.filter(
            important_topic_id=topic_id, fk_user_id=user_id, important_topic_deleted_at__isnull=True
        ).first()
        if not topic:
            return 404, "Not found or not yours.", None
        if payload.get("subject_code") and payload.get("subject_name"):
            topic.fk_subject = SubjectManagement.get_or_create(
                payload["subject_code"], payload["subject_name"]
            )
        if "faculty_name" in payload:
            topic.fk_faculty = _get_faculty(payload["faculty_name"])
        for field in ("important_topic_title", "important_topic_exam_type"):
            if field in payload:
                setattr(topic, field, payload[field])
        topic.save()
        return 200, "Updated.", {"important_topic_id": str(topic.important_topic_id)}

    @staticmethod
    def delete(user_id: str, topic_id: str) -> tuple[int, str, dict | None]:
        topic = ImportantTopics.objects.filter(
            important_topic_id=topic_id, fk_user_id=user_id, important_topic_deleted_at__isnull=True
        ).first()
        if not topic:
            return 404, "Not found or not yours.", None
        topic.important_topic_deleted_at = timezone.now()
        topic.save(update_fields=["important_topic_deleted_at"])
        return 200, "Deleted.", None
