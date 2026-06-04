"""
Central ORM models for PaperRepo.
All Django models live here. App `models.py` files hold business-logic
service classes only (no ORM models there).
"""

import uuid

from django.db import models


# ---------------------------------------------------------------------------
# Enum choices
# ---------------------------------------------------------------------------

class ExamType(models.TextChoices):
    CAT_I = "CAT I", "CAT I"
    CAT_II = "CAT II", "CAT II"
    FAT = "FAT", "FAT"


class Semester(models.TextChoices):
    FALL = "FALL SEM", "FALL SEM"
    WIN = "WIN SEM", "WIN SEM"
    OTHERS = "Others", "Others"


class ExamSlot(models.TextChoices):
    A1 = "A1", "A1"
    A2 = "A2", "A2"
    B1 = "B1", "B1"
    B2 = "B2", "B2"
    C1 = "C1", "C1"
    C2 = "C2", "C2"
    D1 = "D1", "D1"
    D2 = "D2", "D2"
    E1 = "E1", "E1"
    E2 = "E2", "E2"
    F1 = "F1", "F1"
    F2 = "F2", "F2"
    G1 = "G1", "G1"
    G2 = "G2", "G2"


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class UserInfo(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_email = models.CharField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255)
    user_password_hash = models.CharField(max_length=255)
    user_is_active = models.BooleanField(default=True)
    user_last_login_at = models.DateTimeField(null=True, default=None)
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_updated_at = models.DateTimeField(auto_now=True)
    user_deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "user_info"
        managed = True

    def __str__(self) -> str:
        return self.user_email


# ---------------------------------------------------------------------------
# Lookup tables (normalization)
# ---------------------------------------------------------------------------

class Subjects(models.Model):
    subject_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=200)
    subject_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subjects"
        managed = True

    def __str__(self) -> str:
        return f"{self.subject_code} - {self.subject_name}"


class Faculties(models.Model):
    faculty_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty_name = models.CharField(max_length=100, unique=True)
    faculty_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "faculties"
        managed = True

    def __str__(self) -> str:
        return self.faculty_name


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

class QuestionPapers(models.Model):
    question_paper_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column="user_id", related_name="question_papers")
    fk_subject = models.ForeignKey(Subjects, on_delete=models.PROTECT, db_column="subject_id", related_name="question_papers")
    question_paper_title = models.CharField(max_length=100)
    question_paper_exam_slot = models.CharField(max_length=2, choices=ExamSlot.choices)
    question_paper_exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    question_paper_semester = models.CharField(max_length=20, choices=Semester.choices)
    question_paper_year = models.IntegerField(default=2017)
    question_paper_file_path = models.CharField(max_length=1024)
    question_paper_created_at = models.DateTimeField(auto_now_add=True)
    question_paper_updated_at = models.DateTimeField(auto_now=True)
    question_paper_deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "question_papers"
        managed = True

    def __str__(self) -> str:
        return self.question_paper_title


class ImportantTopics(models.Model):
    important_topic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column="user_id", related_name="important_topics")
    fk_subject = models.ForeignKey(Subjects, on_delete=models.PROTECT, db_column="subject_id", related_name="important_topics")
    fk_faculty = models.ForeignKey(Faculties, on_delete=models.SET_NULL, db_column="faculty_id", null=True, blank=True, default=None, related_name="important_topics")
    important_topic_title = models.CharField(max_length=100)
    important_topic_exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    important_topic_file_path = models.CharField(max_length=1024)
    important_topic_created_at = models.DateTimeField(auto_now_add=True)
    important_topic_updated_at = models.DateTimeField(auto_now=True)
    important_topic_deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "important_topics"
        managed = True

    def __str__(self) -> str:
        return self.important_topic_title


class Materials(models.Model):
    material_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column="user_id", related_name="materials")
    fk_subject = models.ForeignKey(Subjects, on_delete=models.PROTECT, db_column="subject_id", related_name="materials")
    fk_faculty = models.ForeignKey(Faculties, on_delete=models.SET_NULL, db_column="faculty_id", null=True, blank=True, default=None, related_name="materials")
    material_title = models.CharField(max_length=100)
    material_topic_type = models.CharField(max_length=50)
    material_file_path = models.CharField(max_length=1024)
    material_created_at = models.DateTimeField(auto_now_add=True)
    material_updated_at = models.DateTimeField(auto_now=True)
    material_deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "materials"
        managed = True

    def __str__(self) -> str:
        return self.material_title
