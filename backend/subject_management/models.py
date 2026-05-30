"""Subject lookup business logic. ORM models live in core.client_model_app."""

from core.client_model_app.models import Subjects


class SubjectManagement:
    @staticmethod
    def get_or_create(subject_code: str, subject_name: str) -> Subjects:
        code = subject_code.strip().upper()
        subject, _ = Subjects.objects.get_or_create(
            subject_code=code,
            defaults={"subject_name": subject_name.strip()},
        )
        return subject

    @staticmethod
    def list_subjects(search: str | None = None) -> tuple[int, str, list]:
        qs = Subjects.objects.all().order_by("subject_code")
        if search:
            qs = qs.filter(subject_code__icontains=search.strip().upper())
        data = [
            {
                "subject_id": str(s.subject_id),
                "subject_code": s.subject_code,
                "subject_name": s.subject_name,
            }
            for s in qs
        ]
        return 200, "OK", data
