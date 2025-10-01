from django.db import models
from django.contrib.auth.models import User

EXAM_CHOICES = [("CAT I", "CAT I"),("CAT II", "CAT II"),("FAT", "FAT")]

SEM_CHOICES = [("FALL SEM", "FALL SEM"),("WIN SEM", "WIN SEM"),("Others", "Others")]

class QuestionPapers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_paper_id = models.AutoField(primary_key=True)
    question_paper_title = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=20)
    exam_slot = models.CharField(max_length = 2)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    semester = models.CharField(max_length=20, choices=SEM_CHOICES)
    year = models.IntegerField(default=2017)
    file_choosen = models.FileField(upload_to="QuestionPapers/")
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.subject_name} ({self.exam_type})"


class ImportantTopics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    important_topic_id = models.AutoField(primary_key=True)
    important_topic_title = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=20)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    faculty_name = models.CharField(max_length=50 , null = True , blank = True)
    file_choosen = models.FileField(upload_to="ImportantTopics/")
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.subject_name} ({self.faculty_name})"


class Materials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material_id = models.AutoField(primary_key=True)
    study_material_title = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=20)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    faculty_name = models.CharField(max_length=50 , null = True , blank = True)
    file_choosen = models.FileField(upload_to="Materials/")
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.subject_name} ({self.faculty_name})"
