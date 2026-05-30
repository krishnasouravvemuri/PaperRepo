from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from src.utils.response import ApiResponse

from .models import ImportantTopicManagement
from .serializers import CreateImportantTopicSerializer, UpdateImportantTopicSerializer


def _require_auth(request):
    return request.META.get("user_id")


class ImportantTopicListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        filters = {
            "course_code": request.query_params.get("course_code"),
            "exam_type": request.query_params.get("exam_type"),
        }
        code, message, data = ImportantTopicManagement.list_topics(filters=filters)
        return ApiResponse(data, code, message).build()

    def post(self, request):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        serializer = CreateImportantTopicSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()
        files = serializer.validated_data.pop("files")
        code, message, data = ImportantTopicManagement.create(user_id, serializer.validated_data, files)
        return ApiResponse(data, code, message).build()


class MyImportantTopicsView(APIView):
    def get(self, request):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = ImportantTopicManagement.list_mine(user_id=user_id)
        return ApiResponse(data, code, message).build()


class ImportantTopicDetailView(APIView):
    def patch(self, request, topic_id):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        serializer = UpdateImportantTopicSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()
        code, message, data = ImportantTopicManagement.update(
            user_id, str(topic_id), serializer.validated_data
        )
        return ApiResponse(data, code, message).build()

    def delete(self, request, topic_id):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = ImportantTopicManagement.delete(user_id, str(topic_id))
        return ApiResponse(data, code, message).build()


class ImportantTopicFileView(APIView):
    def get(self, request, topic_id):
        code, message, data = ImportantTopicManagement.get_file_url(str(topic_id))
        return ApiResponse(data, code, message).build()
