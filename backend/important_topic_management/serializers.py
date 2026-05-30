from rest_framework import serializers

from core.client_model_app.models import ExamType


class CreateImportantTopicSerializer(serializers.Serializer):
    important_topic_title = serializers.CharField(max_length=100)
    subject_code = serializers.CharField(max_length=20)
    subject_name = serializers.CharField(max_length=200)
    important_topic_exam_type = serializers.ChoiceField(choices=ExamType.choices)
    faculty_name = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False, write_only=True)


class UpdateImportantTopicSerializer(serializers.Serializer):
    important_topic_title = serializers.CharField(max_length=100, required=False)
    subject_code = serializers.CharField(max_length=20, required=False)
    subject_name = serializers.CharField(max_length=200, required=False)
    important_topic_exam_type = serializers.ChoiceField(choices=ExamType.choices, required=False)
    faculty_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
