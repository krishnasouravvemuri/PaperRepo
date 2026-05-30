"""Question paper business logic. ORM models live in core.client_model_app."""

from django.utils import timezone

from core.client_model_app.models import QuestionPapers
from src.common.blob import BlobClient
from src.common.blob_paths import BlobPaths
from subject_management.models import SubjectManagement


def _serialize(p: QuestionPapers) -> dict:
    return {
        "question_paper_id": str(p.question_paper_id),
        "question_paper_title": p.question_paper_title,
        "subject_code": p.fk_subject.subject_code,
        "subject_name": p.fk_subject.subject_name,
        "question_paper_exam_slot": p.question_paper_exam_slot,
        "question_paper_exam_type": p.question_paper_exam_type,
        "question_paper_semester": p.question_paper_semester,
        "question_paper_year": p.question_paper_year,
        "uploaded_by": p.fk_user.user_name,
    }


class QuestionPaperManagement:
    @staticmethod
    def create(user_id: str, payload: dict, files: list) -> tuple[int, str, dict | None]:
        subject = SubjectManagement.get_or_create(payload["subject_code"], payload["subject_name"])
        created = []
        for f in files:
            path = BlobPaths.question_paper(user_id, f.name)
            BlobClient.upload(path, f.read(), getattr(f, "content_type", "application/octet-stream"))
            paper = QuestionPapers.objects.create(
                fk_user_id=user_id,
                fk_subject=subject,
                question_paper_title=payload["question_paper_title"],
                question_paper_exam_slot=payload["question_paper_exam_slot"],
                question_paper_exam_type=payload["question_paper_exam_type"],
                question_paper_semester=payload["question_paper_semester"],
                question_paper_year=payload["question_paper_year"],
                question_paper_file_path=path,
            )
            created.append(str(paper.question_paper_id))
        return 201, f"{len(created)} file(s) uploaded.", {"created_ids": created}

    @staticmethod
    def list_papers(filters: dict) -> tuple[int, str, list]:
        qs = (
            QuestionPapers.objects.filter(question_paper_deleted_at__isnull=True)
            .select_related("fk_subject", "fk_user")
            .order_by("-question_paper_created_at")
        )
        if filters.get("course_code"):
            qs = qs.filter(fk_subject__subject_code__icontains=filters["course_code"].strip().upper())
        if filters.get("exam_type"):
            qs = qs.filter(question_paper_exam_type=filters["exam_type"])
        return 200, "OK", [_serialize(p) for p in qs]

    @staticmethod
    def list_mine(user_id: str) -> tuple[int, str, list]:
        qs = (
            QuestionPapers.objects.filter(fk_user_id=user_id, question_paper_deleted_at__isnull=True)
            .select_related("fk_subject", "fk_user")
            .order_by("-question_paper_created_at")
        )
        return 200, "OK", [_serialize(p) for p in qs]

    @staticmethod
    def get_file_url(paper_id: str) -> tuple[int, str, dict | None]:
        paper = QuestionPapers.objects.filter(
            question_paper_id=paper_id, question_paper_deleted_at__isnull=True
        ).first()
        if not paper:
            return 404, "Not found.", None
        return 200, "OK", {"url": BlobClient.signed_url(paper.question_paper_file_path)}

    @staticmethod
    def update(user_id: str, paper_id: str, payload: dict) -> tuple[int, str, dict | None]:
        paper = QuestionPapers.objects.filter(
            question_paper_id=paper_id, fk_user_id=user_id, question_paper_deleted_at__isnull=True
        ).first()
        if not paper:
            return 404, "Not found or not yours.", None

        if payload.get("subject_code") and payload.get("subject_name"):
            paper.fk_subject = SubjectManagement.get_or_create(
                payload["subject_code"], payload["subject_name"]
            )
        for field in (
            "question_paper_title",
            "question_paper_exam_slot",
            "question_paper_exam_type",
            "question_paper_semester",
            "question_paper_year",
        ):
            if field in payload:
                setattr(paper, field, payload[field])
        paper.save()
        return 200, "Updated.", {"question_paper_id": str(paper.question_paper_id)}

    @staticmethod
    def delete(user_id: str, paper_id: str) -> tuple[int, str, dict | None]:
        paper = QuestionPapers.objects.filter(
            question_paper_id=paper_id, fk_user_id=user_id, question_paper_deleted_at__isnull=True
        ).first()
        if not paper:
            return 404, "Not found or not yours.", None
        paper.question_paper_deleted_at = timezone.now()
        paper.save(update_fields=["question_paper_deleted_at"])
        return 200, "Deleted.", None
