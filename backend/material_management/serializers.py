from rest_framework import serializers


class CreateMaterialSerializer(serializers.Serializer):
    material_title = serializers.CharField(max_length=100)
    subject_code = serializers.CharField(max_length=20)
    subject_name = serializers.CharField(max_length=200)
    material_topic_type = serializers.CharField(max_length=50)
    faculty_name = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False, write_only=True)


class UpdateMaterialSerializer(serializers.Serializer):
    material_title = serializers.CharField(max_length=100, required=False)
    subject_code = serializers.CharField(max_length=20, required=False)
    subject_name = serializers.CharField(max_length=200, required=False)
    material_topic_type = serializers.CharField(max_length=50, required=False)
    faculty_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
