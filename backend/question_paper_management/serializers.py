from rest_framework import serializers

from core.client_model_app.models import ExamType, Semester


class CreateQuestionPaperSerializer(serializers.Serializer):
    question_paper_title = serializers.CharField(max_length=100)
    subject_code = serializers.CharField(max_length=20)
    subject_name = serializers.CharField(max_length=200)
    question_paper_exam_slot = serializers.CharField(max_length=10)
    question_paper_exam_type = serializers.ChoiceField(choices=ExamType.choices)
    question_paper_semester = serializers.ChoiceField(choices=Semester.choices)
    question_paper_year = serializers.IntegerField(min_value=1990, max_value=2100)
    files = serializers.ListField(
        child=serializers.FileField(), allow_empty=False, write_only=True
    )


class UpdateQuestionPaperSerializer(serializers.Serializer):
    question_paper_title = serializers.CharField(max_length=100, required=False)
    subject_code = serializers.CharField(max_length=20, required=False)
    subject_name = serializers.CharField(max_length=200, required=False)
    question_paper_exam_slot = serializers.CharField(max_length=10, required=False)
    question_paper_exam_type = serializers.ChoiceField(choices=ExamType.choices, required=False)
    question_paper_semester = serializers.ChoiceField(choices=Semester.choices, required=False)
    question_paper_year = serializers.IntegerField(min_value=1990, max_value=2100, required=False)
