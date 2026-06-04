"""Study material business logic. ORM models live in core.client_model_app."""

from django.utils import timezone

from core.client_model_app.models import Faculties, Materials
from src.common.blob import BlobClient
from src.common.blob_paths import BlobPaths, download_name
from subject_management.models import SubjectManagement


def _get_faculty(faculty_name: str | None) -> Faculties | None:
    name = (faculty_name or "").strip()
    if not name:
        return None
    faculty, _ = Faculties.objects.get_or_create(faculty_name=name)
    return faculty


def _serialize(m: Materials) -> dict:
    return {
        "material_id": str(m.material_id),
        "material_title": m.material_title,
        "subject_code": m.fk_subject.subject_code,
        "subject_name": m.fk_subject.subject_name,
        "material_topic_type": m.material_topic_type,
        "faculty_name": m.fk_faculty.faculty_name if m.fk_faculty else "",
        "uploaded_by": m.fk_user.user_name,
    }


class MaterialManagement:
    @staticmethod
    def create(user_id: str, payload: dict, files: list) -> tuple[int, str, dict | None]:
        subject = SubjectManagement.get_or_create(payload["subject_code"], payload["subject_name"])
        faculty = _get_faculty(payload.get("faculty_name"))
        created = []
        for f in files:
            path = BlobPaths.material(user_id, f.name)
            BlobClient.upload(path, f.read(), getattr(f, "content_type", "application/octet-stream"))
            material = Materials.objects.create(
                fk_user_id=user_id,
                fk_subject=subject,
                fk_faculty=faculty,
                material_title=payload["material_title"],
                material_topic_type=payload["material_topic_type"],
                material_file_path=path,
            )
            created.append(str(material.material_id))
        return 201, f"{len(created)} file(s) uploaded.", {"created_ids": created}

    @staticmethod
    def list_materials(filters: dict) -> tuple[int, str, list]:
        qs = (
            Materials.objects.filter(material_deleted_at__isnull=True)
            .select_related("fk_subject", "fk_user", "fk_faculty")
            .order_by("-material_created_at")
        )
        if filters.get("course_code"):
            qs = qs.filter(fk_subject__subject_code__icontains=filters["course_code"].strip().upper())
        if filters.get("topic_type"):
            qs = qs.filter(material_topic_type__icontains=filters["topic_type"])
        return 200, "OK", [_serialize(m) for m in qs]

    @staticmethod
    def list_mine(user_id: str) -> tuple[int, str, list]:
        qs = (
            Materials.objects.filter(fk_user_id=user_id, material_deleted_at__isnull=True)
            .select_related("fk_subject", "fk_user", "fk_faculty")
            .order_by("-material_created_at")
        )
        return 200, "OK", [_serialize(m) for m in qs]

    @staticmethod
    def get_file_url(material_id: str) -> tuple[int, str, dict | None]:
        material = Materials.objects.filter(
            material_id=material_id, material_deleted_at__isnull=True
        ).first()
        if not material:
            return 404, "Not found.", None
        name = download_name(material.material_title, material.material_file_path)
        return 200, "OK", {
            "url": BlobClient.signed_url(material.material_file_path, download=name),
            "filename": name,
        }

    @staticmethod
    def update(user_id: str, material_id: str, payload: dict) -> tuple[int, str, dict | None]:
        material = Materials.objects.filter(
            material_id=material_id, fk_user_id=user_id, material_deleted_at__isnull=True
        ).first()
        if not material:
            return 404, "Not found or not yours.", None
        if payload.get("subject_code") and payload.get("subject_name"):
            material.fk_subject = SubjectManagement.get_or_create(
                payload["subject_code"], payload["subject_name"]
            )
        if "faculty_name" in payload:
            material.fk_faculty = _get_faculty(payload["faculty_name"])
        for field in ("material_title", "material_topic_type"):
            if field in payload:
                setattr(material, field, payload[field])
        material.save()
        return 200, "Updated.", {"material_id": str(material.material_id)}

    @staticmethod
    def delete(user_id: str, material_id: str) -> tuple[int, str, dict | None]:
        material = Materials.objects.filter(
            material_id=material_id, fk_user_id=user_id, material_deleted_at__isnull=True
        ).first()
        if not material:
            return 404, "Not found or not yours.", None
        material.material_deleted_at = timezone.now()
        material.save(update_fields=["material_deleted_at"])
        return 200, "Deleted.", None
